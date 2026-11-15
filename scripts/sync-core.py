"""Build deterministic pure-Python wheel; deliver and check explicit consumers."""
import argparse
import base64
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import zipfile
import tomllib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'packages/core'
VERSION=tomllib.loads((SOURCE/'pyproject.toml').read_text(encoding='utf-8'))['project']['version']
NAME=f'cycling_suite_core-{VERSION}-py3-none-any.whl'

def contents():
    files={str(p.relative_to(SOURCE/'src')).replace('\\','/'):p.read_bytes() for p in (SOURCE/'src').rglob('*.py')}
    dist=f'cycling_suite_core-{VERSION}.dist-info/'
    files.update({dist+'METADATA':f'Metadata-Version: 2.1\nName: cycling-suite-core\nVersion: {VERSION}\nRequires-Python: >=3.12\nLicense: GPL-3.0-or-later\n\nShared runtime primitives derived from Fuorigiri.\n'.encode(),dist+'WHEEL':b'Wheel-Version: 1.0\nGenerator: cycling-suite-common\nRoot-Is-Purelib: true\nTag: py3-none-any\n',dist+'LICENSE':(SOURCE/'LICENSE').read_bytes(),dist+'NOTICE.md':(SOURCE/'NOTICE.md').read_bytes()})
    record=io.StringIO(newline='');writer=csv.writer(record,lineterminator='\n')
    for name,raw in sorted(files.items()):writer.writerow([name,'sha256='+base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip('='),len(raw)])
    writer.writerow([dist+'RECORD','','']);files[dist+'RECORD']=record.getvalue().encode()
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,raw)
    return output.getvalue()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--app',action='append',default=[]);parser.add_argument('--check',action='store_true');parser.add_argument('--install',action='store_true');args=parser.parse_args()
    raw=contents();digest=hashlib.sha256(raw).hexdigest()
    artifact=ROOT/'artifacts'/NAME
    if artifact.exists() and artifact.read_bytes()!=raw:raise ValueError('Versione già prodotta diversa: incrementare VERSION e __version__.')
    if not args.check:artifact.write_bytes(raw)
    for value in args.app:
        app=Path(value).resolve();vendor=app/'vendor';meta=vendor/'suite-core-provenance.json'
        if args.check:
            current=json.loads(meta.read_text(encoding='utf-8'))
            if current['sha256']!=digest or current['artifact']!=NAME or (vendor/NAME).read_bytes()!=raw:raise ValueError('Derivazione common superata: '+str(app))
            interpreter=app/('.venv/Scripts/python.exe' if __import__('os').name=='nt' else '.venv/bin/python')
            subprocess.run([str(interpreter),'scripts/verify_core.py'],cwd=app,check=True)
            continue
        vendor.mkdir(exist_ok=True);(vendor/NAME).write_bytes(raw)
        meta.write_text(json.dumps({'package':'cycling-suite-core','version':VERSION,'artifact':NAME,'sha256':digest,'source':'cycling-suite-common/packages/core','origin':'Fuorigiri transports, credentials and instance lock; GPL-3.0-or-later'},indent=2)+'\n',encoding='utf-8')
        (app/'requirements-common.txt').write_text('vendor/'+NAME+'\n',encoding='utf-8')
        shutil.copyfile(ROOT/'scripts/verify-core.py',app/'scripts/verify_core.py')
        # Hash-checked lock companions (.hashes): never write hashes into requirements-common.txt.
        shutil.copyfile(ROOT/'scripts/lock-hashes.py',app/'scripts/lock_hashes.py')
        project=app/'pyproject.toml';text=project.read_text(encoding='utf-8')
        if re.search(r'cycling-suite-core==[^"\s]+',text):text=re.sub(r'cycling-suite-core==[^"\s]+','cycling-suite-core=='+VERSION,text)
        else:text=text.replace('dependencies = [','dependencies = ["cycling-suite-core=='+VERSION+'", ',1)
        project.write_text(text,encoding='utf-8')
        for requirement in list(app.glob('requirements*.lock'))+list(app.glob('requirements*.txt')):
            if requirement.name=='requirements-common.txt':continue
            text=requirement.read_text(encoding='utf-8')
            if '-r requirements-common.txt' not in text:requirement.write_text(text.rstrip()+'\n-r requirements-common.txt\n',encoding='utf-8')
        if args.install:
            interpreter=app/('.venv/Scripts/python.exe' if __import__('os').name=='nt' else '.venv/bin/python')
            subprocess.run([str(interpreter),'-m','pip','install','--no-deps','--no-index','--force-reinstall',str(vendor/NAME)],cwd=app,check=True)
            subprocess.run([str(interpreter),'scripts/verify_core.py'],cwd=app,check=True)
        print('Consegnato common Python '+VERSION+' a '+str(app))

if __name__=='__main__':main()
