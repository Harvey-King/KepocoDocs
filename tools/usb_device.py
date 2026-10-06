"""Run and upload single-file Kepoco games using MicroPython's mpremote."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys


def select_device(device='auto', ports=None):
    if device != 'auto':
        return device
    if ports is None:
        from serial.tools.list_ports import comports
        ports = list(comports())
    candidates = [p.device for p in ports if (p.vid,p.pid)==(0x2e8a,0x0005)]
    if len(candidates) != 1:
        raise ValueError('Expected one RP2040 MicroPython USB device; found '+str(len(candidates))+'. Use list, then --device PORT or a USB serial selector. Disconnect the web editor first.')
    return candidates[0]


def command(action, device, file=None):
    base=[sys.executable,'-m','mpremote','connect',device]
    if action=='run':
        path=Path(file).resolve()
        if not path.is_file() or path.suffix.lower()!='.py':
            raise ValueError('Select an existing .py game file.')
        return base+['soft-reset','run',str(path)]
    if action=='info':
        return base+['exec',"import sys,os; print(sys.implementation); print(os.uname()); print(os.listdir('/Games'))"]
    if action=='repl': return base+['repl']
    if action=='menu': return base+['reset']
    raise ValueError('Unknown action: '+action)


def destination(file):
    path=Path(file).resolve()
    # Enumerate archived filenames only; never import or execute firmware.
    source_library=Path(__file__).resolve().parents[1]/'source-library'
    firmware_names={source.stem.lower() for source in source_library.rglob('*.py')}
    firmware_names.update(('main','boot','kepoco','thumby'))
    if (not path.is_file() or path.suffix.lower()!='.py'
            or any(part.lower() in ('source-library','vendor','typings')
                   for part in path.parent.parts)
            or path.stem.lower() in firmware_names
            or not path.stem.isascii()
            or not all(c.isalnum() or c=='_' for c in path.stem)):
        raise ValueError('Upload only a game .py with a simple name, not firmware or startup files.')
    return '/Games/'+path.stem+'/'+path.name


def upload(file,device):
    target=destination(file)
    base=[sys.executable,'-m','mpremote','connect',device]
    folder=target.rsplit('/',1)[0]
    mkdir="import os\ntry:\n os.mkdir("+repr(folder)+")\nexcept OSError as e:\n if e.args[0] != 17: raise"
    subprocess.run(base+['exec',mkdir],check=True)
    subprocess.run(base+['fs','cp',str(Path(file).resolve()),':'+target],check=True)
    code="import hashlib,binascii; print(binascii.hexlify(hashlib.sha256(open("+repr(target)+",'rb').read()).digest()).decode())"
    result=subprocess.run(base+['exec',code],capture_output=True,text=True,check=True)
    expected=hashlib.sha256(Path(file).read_bytes()).hexdigest()
    if result.stdout.strip()!=expected:
        raise RuntimeError('Remote SHA-256 differs from local file. Upload NOT verified.')
    print('Uploaded and SHA-256 verified:',target)
    return 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['run','upload','info','repl','menu','list'])
    parser.add_argument('file',nargs='?')
    parser.add_argument('--device',default='auto',help='auto, COM port, or mpremote USB serial selector')
    args=parser.parse_args()
    try:
        if args.action=='list':
            return subprocess.run([sys.executable,'-m','mpremote','connect','list']).returncode
        if args.action in ('run','upload') and args.file is None:
            parser.error('run/upload requires a saved .py file')
        device=select_device(args.device)
        if args.action=='upload': return upload(args.file,device)
        return subprocess.run(command(args.action,device,args.file)).returncode
    except ImportError:
        print('Install dependencies in this Python environment: python -m pip install -r requirements-dev.txt',file=sys.stderr)
        return 1
    except (ValueError,RuntimeError,subprocess.CalledProcessError) as exc:
        print('Kepoco USB: '+str(exc),file=sys.stderr)
        print('Disconnect the web editor and stop other USB tasks before retrying.',file=sys.stderr)
        return 1

if __name__=='__main__': sys.exit(main())
