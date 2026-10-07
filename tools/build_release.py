"""Build an auditable VSIX and portable archive; never import firmware."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
GUIDES=('readme.md','GETTING_STARTED.md','FEATURE_GUIDE.md','API_REFERENCE.md','FIRMWARE_NOTES.md','USB_WORKFLOW.md','CONTRIBUTING.md','CHANGELOG.md','THIRD_PARTY_NOTICES.md')


def stage():
    assets=ROOT/'vscode-extension/assets'
    # Only this generated tree is builder-owned; leave original inputs intact.
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True,exist_ok=True)
    for name in ('typings','vendor/micropython','source-library','examples','evidence'):
        shutil.copytree(ROOT/name,assets/name,dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pyo'))
    docs=assets/'docs'
    docs.mkdir(exist_ok=True)
    # Preserve relative navigation when root guides are bundled inside docs.
    shutil.copytree(ROOT/'assets',docs/'assets',dirs_exist_ok=True)
    shutil.copytree(ROOT/'examples',docs/'examples',dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pyo'))
    shutil.copy2(ROOT/'swerve.py',docs/'swerve.py')
    shutil.copy2(ROOT/'LICENSE',docs/'LICENSE')
    for name in GUIDES:
        text=(ROOT/name).read_text(encoding='utf-8')
        text=text.replace('](source-library/','](../source-library/').replace('](evidence/','](../evidence/')
        (docs/name).write_text(text,encoding='utf-8')
    # The catalogue is bundled twice: docs/examples keeps repository links,
    # while assets/examples must navigate through the sibling docs directory.
    catalogue=assets/'examples/README.md'
    if catalogue.is_file():
        text=catalogue.read_text(encoding='utf-8')
        for name in (*GUIDES,'swerve.py'):
            text=text.replace('](../'+name+')','](../docs/'+name+')')
        catalogue.write_text(text,encoding='utf-8')
    for name in ('LICENSE','THIRD_PARTY_NOTICES.md'):
        shutil.copy2(ROOT/name,ROOT/'vscode-extension'/name)
    shutil.copytree(ROOT/'licenses',ROOT/'vscode-extension/licenses',dirs_exist_ok=True)
    sources=json.loads((ROOT/'evidence/SOURCE_MANIFEST.json').read_text())['sources']
    for item in sources:
        if hashlib.sha256((assets/'source-library'/item['name']).read_bytes()).hexdigest()!=item['sha256']:
            raise RuntimeError('Source snapshot digest mismatch: '+item['name'])
    return assets


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage-only',action='store_true')
    args=parser.parse_args()
    stage()
    if args.stage_only:
        print('Staged verified extension assets.')
        return
    version=json.loads((ROOT/'vscode-extension/package.json').read_text())['version']
    dist=ROOT/'dist'
    dist.mkdir(exist_ok=True)
    vsix=dist/('kepoco-devkit-'+version+'.vsix')
    cli=ROOT/'node_modules/@vscode/vsce/vsce'
    if not cli.exists(): raise SystemExit('Run npm ci first to install the release builder.')
    subprocess.run(['node',str(cli),'package','--out',str(vsix)],cwd=ROOT/'vscode-extension',check=True)
    with zipfile.ZipFile(vsix) as archive:
        names=set(archive.namelist())
        for required in ('extension/package.json','extension/LICENSE.txt','extension/assets/docs/USB_WORKFLOW.md','extension/assets/typings/kepoco/__init__.pyi'):
            if required not in names: raise RuntimeError('Missing packaged asset: '+required)
    portable=dist/('Kepoco-DevKit-'+version+'.zip')
    # Ship tracked and nonignored project files only; never .venv, caches or machine reports.
    result=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True,check=True)
    with zipfile.ZipFile(portable,'w',zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(set(result.stdout.decode().split('\0'))- {''}):
            path=ROOT/relative
            if path.is_file() and not relative.endswith('.vsix'):
                archive.write(path,'KepocoDocs/'+relative)
        archive.write(vsix,'KepocoDocs/'+vsix.name)
    checksums=dist/'SHA256SUMS.txt'
    checksums.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in (vsix,portable)),encoding='ascii')
    print('Verified VSIX:',vsix)
    print('Portable project:',portable)
    print('Checksums:',checksums)

if __name__=='__main__': main()
