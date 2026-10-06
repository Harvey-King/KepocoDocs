"""Index Kepoco source without importing or executing hardware modules."""
import ast
import hashlib
import json
from pathlib import Path
import warnings

EXTRA_MODULES = {'dummyScreen', 'ssd1306', 'demo'}

def parse_source(path):
    text = path.read_text(encoding='utf-8-sig')
    warning = None
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', SyntaxWarning)
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as error:
            lines = text.splitlines()
            if path.name != 'kepocoVGA.py' or error.lineno != 223 or 'return list(sorted(' not in lines[222]:
                raise
            warning = {'line': error.lineno, 'message': error.msg,
                       'action': 'Only this function-body line replaced by return None in the in-memory index. Original file unchanged.'}
            lines[222] = '        return None  # INDEX-ONLY placeholder for malformed expression'
            tree = ast.parse('\n'.join(lines), filename=str(path))
    return text, tree, warning

def scope_nodes(body):
    """Visit declarations through conditional branches, never function bodies."""
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
            yield node
        elif isinstance(node, (ast.If, ast.For, ast.While, ast.With)):
            yield from scope_nodes(node.body)
            yield from scope_nodes(getattr(node, 'orelse', []))
        elif isinstance(node, ast.Try):
            yield from scope_nodes(node.body)
            for handler in node.handlers:
                yield from scope_nodes(handler.body)
            yield from scope_nodes(node.orelse)
            yield from scope_nodes(node.finalbody)

def source_doc(text, node):
    doc = ast.get_docstring(node)
    if doc:
        return doc
    lines = text.splitlines()
    start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])]) - 2
    comments = []
    while start >= 0 and lines[start].strip().startswith('#'):
        comments.insert(0, lines[start].strip().lstrip('#').strip())
        start -= 1
    return '\n'.join(comments)

def function_record(text, node):
    return {'name': node.name, 'line': node.lineno,
            'signature': node.name + '(' + ast.unparse(node.args) + ')',
            'parameters': [a.arg for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs],
            'doc': source_doc(text, node)}

def index_sources(directory):
    result = []
    files = sorted(p for p in Path(directory).glob('*.py')
                   if p.stem.startswith(('kepoco', 'thumby')) or p.stem in EXTRA_MODULES)
    for path in files:
        text, tree, warning = parse_source(path)
        nodes = list(scope_nodes(tree.body))
        classes = []
        functions = []
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                classes.append({'name': node.name, 'line': node.lineno,
                    'bases': [ast.unparse(b) for b in node.bases],
                    'methods': [function_record(text, m) for m in scope_nodes(node.body)
                                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]})
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(function_record(text, node))
        result.append({'name': path.name, 'module': path.stem, 'source_path': str(path.resolve()),
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'line_count': len(text.splitlines()), 'parse_warning': warning,
                       'classes': classes, 'functions': functions})
    return result

# Inferred/editor-only types. Names/defaults always come from source AST.
PARAM_TYPES = {
    'x': 'int', 'y': 'int', 'x0': 'int', 'y0': 'int', 'x1': 'int', 'y1': 'int',
    'width': 'int', 'height': 'int', 'colour': 'int', 'color': 'int', 'key': 'int',
    'frame': 'int', 'duration': 'int', 'freq': 'int', 'newFrameRate': 'float',
    'mirrorX': 'bool | int', 'mirrorY': 'bool | int', 'space': 'int',
    'fontFile': 'str', 'stringToPrint': 'str | bytes | bytearray | memoryview',
    'subdir': 'str', 'red': 'int', 'green': 'int', 'blue': 'int',
    'rotation': 'int', 'rot': 'int', 'alignX': 'str', 'alignY': 'str',
    'refreshRate': 'float | None', 'setting': 'int', 'contrast': 'int',
    'inverted': 'bool', 'backup': 'bool', 'bitmapData': 'BitmapData',
}
RETURN_TYPES = {
    ('ButtonClass', 'pressed'): 'bool', ('ButtonClass', 'justPressed'): 'bool',
    ('Sprite', 'getFrame'): 'int', ('SavesClass', 'hasItem'): 'bool',
    ('SavesClass', 'getName'): 'str', ('LinkClass', 'send'): 'bool | None',
    ('LinkClass', 'receive'): 'bytes | None', ('VGADriver', 'detect_vga'): 'bool',
    ('VGADriver', 'read_edid'): 'dict[str, Any] | None',
    ('VGADriver', 'supported_refresh_rates'): 'list[int]',
    ('Configuration', 'toKey'): 'str', ('Configuration', 'settings'): 'list[str]',
    ('Configuration', 'allSettings'): 'list[str]',
    ('', 'inputPressed'): 'bool', ('', 'inputJustPressed'): 'bool',
    ('', 'dpadPressed'): 'bool', ('', 'dpadJustPressed'): 'bool',
    ('', 'actionPressed'): 'bool', ('', 'actionJustPressed'): 'bool',
    ('', 'detect_vga'): 'bool',
}
HELP = {
    ('DisplayInterface', 'update'): 'Present the buffer and enforce the frame-rate cap. While waiting, button edges are latched. Does not return a frame count.',
    ('DisplayInterface', 'setFPS'): 'Set the requested FPS, clamped to 0..60 in this library. Zero disables frame limiting; actual delivered FPS may be lower.',
    ('DisplayInterface', 'getPixel'): 'WARNING: this wrapper calls driver.getPixel but does not return it. In the supplied source this returns None, not a pixel colour.',
    ('DisplayInterface', 'drawText'): 'Draw text with the selected bitmap font. This source constructs memoryview(stringToPrint); bytes are a safer choice when porting across runtimes. Call update to show it.',
    ('DisplayInterface', 'setFont'): 'Load a .bin font; width and height can be inferred from a fontWIDTHxHEIGHT filename. space is inter-character spacing. The file must exist on the target.',
    ('DisplayInterface', 'drawEllispe'): 'Exact source spelling: Ellispe, not Ellipse. Delegates to the active driver; the base driver may raise NotImplementedError.',
    ('DisplayInterface', 'drawFilledEllispe'): 'Exact source spelling: Ellispe, not Ellipse. Draw a filled ellipse through the current driver.',
    ('DisplayInterface', 'drawSprite'): 'Draw a Sprite using its bitmap, position, key and mirror fields. Rendering remains in the buffer until update/show.',
    ('DisplayInterface', 'drawSpriteWithMask'): 'Draw sprite s with sprite m as its mask. Both arguments must expose bitmap data.',
    ('DisplayInterface', 'setModeGreyscale'): 'Select four-tone greyscale if supported by the active driver. Support is backend-dependent.',
    ('ButtonClass', 'justPressed'): 'Return a new or latched button edge and consume the latch. Read once per frame and store the result if multiple systems need it.',
    ('Sprite', '__init__'): 'Create a sprite from bytearray data or a filename. Two matching bitplanes may be supplied as a tuple/list. Frame byte size is width * ceil(height/8).',
    ('Sprite', 'setFrame'): 'Select an animation frame modulo frameCount. Negative indices do not update the frame.',
    ('AudioClass', 'play'): 'Play frequency freq (Hz) for duration milliseconds without waiting for completion. Requires a working audio backend.',
    ('AudioClass', 'playBlocking'): 'Play a tone and busy-wait for duration milliseconds, blocking gameplay. Requires a working audio backend.',
    ('SavesClass', 'setItem'): 'Set a value in the in-memory save dictionary. Use save() to persist. Keys beginning __b are reserved for byte metadata.',
    ('SavesClass', 'getItem'): 'Get a saved value, decoding stored byte data if needed; returns None when missing.',
    ('SavesClass', 'setName'): 'Select a game-specific save directory under /Saves and load its persistent or backup JSON.',
    ('SavesClass', 'save'): 'Write the in-memory dictionary to persistent.json. backup=True renames the prior file to backup.json first.',
    ('LinkClass', 'send'): 'Physical branch sends up to 512 bytes and returns success/failure. Emulator/colour branches are no-ops returning None.',
    ('LinkClass', 'receive'): 'Physical branch receives a checked packet or None. Emulator/colour branches are no-ops returning None.',
    ('Configuration', 'getValues'): 'WARNING: the final fallback uses the undefined name Nones in the supplied file. That branch raises NameError.',
    ('VGADriver', 'supported_refresh_rates'): 'WARNING: the downloaded implementation has a syntax error at line 223. The stub describes the intended callable signature, not a repaired driver.',
}


def inferred_value(node, known_classes=None):
    if isinstance(node, ast.Constant):
        if node.value is None: return 'Any'
        return {bool:'bool', int:'int', float:'float', str:'str', bytes:'bytes'}.get(type(node.value), 'Any')
    if isinstance(node, ast.UnaryOp): return inferred_value(node.operand, known_classes)
    if isinstance(node, ast.List): return 'list[Any]'
    if isinstance(node, ast.Tuple): return 'tuple[Any, ...]'
    if isinstance(node, ast.Dict): return 'dict[Any, Any]'
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id
        if name == 'const' and node.args: return inferred_value(node.args[0], known_classes)
        if name in ('bytearray', 'bytes', 'memoryview', 'str', 'int', 'float', 'bool'): return name
        if known_classes and name in known_classes: return name
    return 'Any'


def return_type(fn, owner):
    if fn.name == '__init__': return 'None'
    if (owner, fn.name) in RETURN_TYPES: return RETURN_TYPES[owner, fn.name]
    if fn.returns and ast.unparse(fn.returns) in ('bool', 'int', 'float', 'str', 'None'):
        return ast.unparse(fn.returns)
    returns = [n.value for n in ast.walk(fn) if isinstance(n, ast.Return) and n.value is not None]
    if not returns: return 'None'
    types = {inferred_value(n) for n in returns}
    return next(iter(types)) if len(types) == 1 and 'Any' not in types else 'Any'


def param_type(arg, default, owner, local_types):
    if arg.arg in ('self', 'cls'): return None
    if owner == 'DisplayInterface' and arg.arg == 'driver': return 'DisplayDriver'
    if owner == 'DisplayInterface' and arg.arg in ('s', 'm'): return 'Sprite'
    if owner == 'SavesClass' and arg.arg == 'key': return 'str'
    if owner == 'Configuration' and arg.arg == 'key': return 'str | int'
    if arg.arg == 'buttons': return 'Iterable[ButtonClass]'
    if arg.annotation:
        annotation = ast.unparse(arg.annotation)
        if annotation in ('int','str','float','bool','bytes','tuple[int, int]','Pin','SPI') or annotation in local_types:
            typ = annotation
        else: typ = 'Any'
    else: typ = PARAM_TYPES.get(arg.arg, 'Any')
    if default and isinstance(default, ast.Constant) and default.value is None and typ not in ('Any',) and 'None' not in typ:
        typ += ' | None'
    return typ


def arguments(fn, owner, local_types):
    args = fn.args
    positional = args.posonlyargs + args.args
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    pieces = []
    for i, (arg, default) in enumerate(zip(positional, defaults)):
        part = arg.arg
        annotation = param_type(arg, default, owner, local_types)
        if annotation: part += ': ' + annotation
        if default is not None:
            part += ' = ' + (ast.unparse(default) if isinstance(default, (ast.Constant, ast.UnaryOp)) else '...')
        pieces.append(part)
        if args.posonlyargs and i == len(args.posonlyargs) - 1: pieces.append('/')
    if args.vararg:
        pieces.append('*' + args.vararg.arg + ': Any')
    elif args.kwonlyargs:
        pieces.append('*')
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        part = arg.arg + ': ' + (param_type(arg, default, owner, local_types) or 'Any')
        if default is not None: part += ' = ' + (ast.unparse(default) if isinstance(default, (ast.Constant,ast.UnaryOp)) else '...')
        pieces.append(part)
    if args.kwarg: pieces.append('**' + args.kwarg.arg + ': Any')
    return ', '.join(pieces)


def method_stub(fn, owner, module, text, local_types, indent=''):
    result = []
    for decorator in fn.decorator_list:
        name = ast.unparse(decorator)
        if name in ('classmethod','staticmethod','property') or name.endswith('.setter'):
            result.append(indent + '@' + name)
    description = HELP.get((owner, fn.name)) or source_doc(text, fn)
    if not description:
        description = 'Source-declared ' + ('method' if owner else 'function') + ': ' + function_record(text, fn)['signature'] + '.'
    description += '\nSource: ' + module + '.py:' + str(fn.lineno) + '. Editor-only hints; not a hardware execution guarantee.'
    result.append(indent + 'def ' + fn.name + '(' + arguments(fn, owner, local_types) + ') -> ' + return_type(fn, owner) + ':')
    result.append(indent + '    ' + repr(description))
    result.append(indent + '    ...')
    return '\n'.join(result)


def render_stub(item, source_dir, source_modules):
    text, tree, _ = parse_source(Path(source_dir)/item['name'])
    nodes = list(scope_nodes(tree.body))
    classes = {}
    functions = {}
    imported = {}
    variables = {}
    for node in nodes:
        if isinstance(node, ast.ClassDef):
            classes.setdefault(node.name, []).append(node)
        elif isinstance(node, ast.FunctionDef):
            functions[node.name] = node
        elif isinstance(node, ast.ImportFrom) and node.module and node.module in source_modules | {'machine', 'utime', 'micropython', 'rp2', 'uctypes'}:
            for alias in node.names:
                if alias.name != '*': imported[alias.asname or alias.name] = (node.module, alias.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and (not target.id.startswith('_') or target.id == '__version__'):
                    variables[target.id] = node.value
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                name = alias.asname or alias.name.split('.')[0]
                if name != '*': variables.setdefault(name, None)
    local_types = set(classes) | set(imported)
    class_types = set(classes) | {name for name in imported if name[:1].isupper()}
    header = '"""Generated from supplied ' + item['name'] + '; source SHA-256 ' + item['sha256'] + '.\n'
    header += 'Source signatures preserved; added types are conservative editor hints. Original sources are in source-library.\n'
    if item['parse_warning']:
        header += 'WARNING: original source syntax failure at line ' + str(item['parse_warning']['line']) + '; index-only body placeholder used.\n'
    header += 'Do not upload these stubs as runtime modules. See THIRD_PARTY_NOTICES.md for source attribution.\n"""\n'
    output = [header, 'from typing import Any, Iterable, TypeAlias']
    output.append('BitmapData: TypeAlias = bytearray | str | tuple[bytearray, bytearray] | tuple[str, str] | list[bytearray] | list[str]')
    if item['module'] == 'thumbyGraphics':
        imported['DisplayDriver'] = ('kepocoDisplayDriver','DisplayDriver')
        imported['Sprite'] = ('thumbySprite','Sprite')
        local_types.update(('DisplayDriver','Sprite'))
    for name, (module, symbol) in sorted(imported.items()):
        output.append('from ' + module + ' import ' + symbol + ' as ' + name)
    for name, definitions in classes.items():
        base = definitions[-1]
        bases = [ast.unparse(b) for b in base.bases if isinstance(b, ast.Name) and b.id in local_types]
        output.append('\nclass ' + name + ('(' + ', '.join(bases) + ')' if bases else '') + ':')
        output.append('    ' + repr('Source class ' + item['name'] + ':' + str(base.lineno) + '. Backend-dependent branches are merged for editing; consult firmware notes.'))
        fields = {}
        methods = {}
        for cls in definitions:
            for node in scope_nodes(cls.body):
                if isinstance(node, ast.FunctionDef): methods[node.name] = node
                elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                    for target in (node.targets if isinstance(node,ast.Assign) else [node.target]):
                        if isinstance(target,ast.Name): fields[target.id] = inferred_value(node.value,class_types)
            for node in ast.walk(cls):
                if isinstance(node, (ast.Assign, ast.AnnAssign)):
                    for target in (node.targets if isinstance(node,ast.Assign) else [node.target]):
                        if isinstance(target,ast.Attribute) and isinstance(target.value,ast.Name) and target.value.id == 'self':
                            typ = inferred_value(node.value,class_types)
                            if isinstance(node.value,ast.Name): typ = PARAM_TYPES.get(node.value.id,'Any')
                            fields[target.attr] = typ
        if name == 'DisplayInterface':
            fields.update({k:'int' for k in ('width','height','font_width','font_height','font_space','font_glyphcnt')})
            fields.update({'driver':'DisplayDriver','display':'DisplayDriver','frameRate':'float','font_bmap':'bytearray'})
        if name == 'Sprite': fields.update({k:'int' for k in ('width','height','x','y','key','frameCount','currentFrame','bitmapByteCount')})
        for field, typ in sorted(fields.items()):
            if field not in methods: output.append('    ' + field + ': ' + typ)
        for fn in methods.values(): output.append('\n' + method_stub(fn,name,item['module'],text,local_types,'    '))
    for fn in functions.values(): output.append('\n' + method_stub(fn,'',item['module'],text,local_types))
    for name, value in sorted(variables.items()):
        if name not in classes and name not in functions and name not in imported and name not in ('Any','Iterable','TypeAlias','BitmapData'):
            output.append(name + ': ' + inferred_value(value,class_types))
    return '\n'.join(output) + '\n'


def build_sdk(source_dir, output_dir):
    import shutil
    source_dir, output_dir = Path(source_dir), Path(output_dir)
    inventory = index_sources(source_dir)
    modules = {item['module'] for item in inventory}
    (output_dir/'docs').mkdir(parents=True,exist_ok=True)
    (output_dir/'source-library').mkdir(parents=True,exist_ok=True)
    for item in inventory:
        target = output_dir/'typings'/item['module']/'__init__.pyi'
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(render_stub(item,source_dir,modules),encoding='utf-8')
        shutil.copy2(source_dir/item['name'],output_dir/'source-library'/item['name'])
    report = {'source_count':len(inventory), 'source_stub_count':len(inventory),
              'source_warning_count':sum(bool(item['parse_warning']) for item in inventory),
              'signature_count':sum(len(i['functions'])+sum(len(c['methods']) for c in i['classes']) for i in inventory)}
    manifest = {'description':'AST-only index; original hardware modules were never imported.',
                'report':report,'sources':inventory}
    (output_dir/'docs/SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    docs = ['# Kepoco source-derived API reference', '',
            'Generated from your downloaded sources. Exact spellings, parameter names and defaults are retained.',
            'Type hints in typings are editor annotations, not guarantees of hardware support.',
            'Backend branches are merged for discoverability; read FIRMWARE_NOTES.md before relying on them.', '',
            '## Module index', '']
    docs.extend('- [' + i['module'] + '](#' + i['module'].lower() + ')' for i in inventory)
    for item in inventory:
        docs += ['', '## ' + item['module'], '',
                 'Source: [source-library/' + item['name'] + '](../source-library/' + item['name'] + ').',
                 'SHA-256: `' + item['sha256'] + '`.', '']
        if item['parse_warning']: docs.append('WARNING: original syntax failure at line ' + str(item['parse_warning']['line']) + '; index-only body placeholder used. The source was not repaired.')
        for cls in item['classes']:
            docs += ['', '### ' + cls['name'] + ' (' + item['name'] + ':' + str(cls['line']) + ')', '']
            for fn in cls['methods']:
                docs.append('- `' + fn['signature'] + '` — ' + (HELP.get((cls['name'],fn['name'])) or fn['doc'] or 'Source-declared method; backend-specific implementation.').replace('\n',' ') + ' [' + item['name'] + ':' + str(fn['line']) + ']')
        for fn in item['functions']:
            docs.append('- `' + fn['signature'] + '` — ' + (HELP.get(('',fn['name'])) or fn['doc'] or 'Source-declared function.').replace('\n',' ') + ' [' + item['name'] + ':' + str(fn['line']) + ']')
    (output_dir/'docs/API_REFERENCE.md').write_text('\n'.join(docs)+'\n',encoding='utf-8')
    return report


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path.home() / 'Downloads')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    print(json.dumps(build_sdk(args.source,args.output) if args.output else index_sources(args.source),indent=2))
