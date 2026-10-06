"""Check public docs, source provenance and deliberately negative type diagnostics."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]


def broken_links(file,text):
    targets=re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)',text)
    targets+=re.findall(r'(?:src|href)="([^"]+)"',text)
    missing=[]
    for target in targets:
        if target.startswith(('https://','http://','mailto:','#','data:')):
            continue
        path=unquote(target.split('#',1)[0])
        if path and not (file.parent/path).exists(): missing.append(target)
    return missing


def main():
    blocks=0
    guides=list(ROOT.glob('*.md'))+[ROOT/'vscode-extension/README.md']
    errors=[]
    for file in guides:
        text=file.read_text(encoding='utf-8')
        for target in broken_links(file,text): errors.append(str(file.relative_to(ROOT))+': '+target)
        if re.search(r'[A-Za-z]:[/\\]Users[/\\]|id:[A-Za-z0-9]{12,}',text): errors.append('Private machine information in '+file.name)
        for block in re.findall(r'```python\s*\n(.*?)```',text,re.S):
            compile(block,file.name,'exec');blocks+=1
    if errors: raise RuntimeError('Documentation errors: '+repr(errors))
    items=json.loads((ROOT/'evidence/SOURCE_MANIFEST.json').read_text())['sources']
    if len(items)!=17: raise RuntimeError('Source inventory must contain 17 files.')
    for item in items:
        data=(ROOT/'source-library'/item['name']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=item['sha256']: raise RuntimeError('Source hash differs: '+item['name'])
        if item['source_path']!='source-library/'+item['name']: raise RuntimeError('Nonportable source path.')
    cli=ROOT/'node_modules/pyright/index.js'
    if not cli.exists(): raise RuntimeError('Run npm ci before repository validation.')
    base=['node',str(cli),'--project',str(ROOT/'pyrightconfig.json'),'--outputjson']
    positive=subprocess.run(base,cwd=ROOT,capture_output=True,text=True)
    report=json.loads(positive.stdout)
    if positive.returncode or report['summary']['errorCount']:
        raise RuntimeError('Positive type check failed: '+positive.stdout)
    negative=subprocess.run(base+[str(ROOT/'tools/fixtures/negative_probe.py')],cwd=ROOT,capture_output=True,text=True)
    report=json.loads(negative.stdout)
    rules={d.get('rule') for d in report['generalDiagnostics']}
    expected={'reportMissingImports','reportUndefinedVariable','reportAttributeAccessIssue','reportCallIssue'}
    if negative.returncode!=1 or not expected<=rules:
        raise RuntimeError('Negative fixture no longer catches required diagnostics: '+repr(rules))
    package=json.loads((ROOT/'package.json').read_text())
    extension=json.loads((ROOT/'vscode-extension/package.json').read_text())
    if package['version']!=extension['version']: raise RuntimeError('Project and extension versions differ.')
    print('PASS: local doc/image links, '+str(blocks)+' Python doc blocks, 17 source hashes, private-path check, versions, positive types and expected negative diagnostics.')

if __name__=='__main__': main()
