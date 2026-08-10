from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest


def git_blob_sha1(path):
    data=path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def main():
    fp=json.loads((ROOT/'freeze/amendment2_fingerprint.json').read_text(encoding='utf-8'))
    if fp.get('scientific_calls_started') is not False: raise SystemExit('FAIL: amendment not pre-outcome')
    failures=[]
    for rel,expected in fp['file_hashes'].items():
        path=ROOT/rel
        if not path.exists(): failures.append(f'missing {rel}'); continue
        got=git_blob_sha1(path)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    manifest=load_manifest(ROOT)
    models=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    if len(manifest)!=fp['expected_prompts_per_model']: failures.append('manifest count mismatch')
    if len(models['models'])!=fp['expected_models']: failures.append('model count mismatch')
    ds=[m for m in models['models'] if m['label']=='deepseek_v32']
    if len(ds)!=1 or ds[0]['provider']!='deepinfra' or ds[0]['reasoning']!='omit': failures.append('DeepSeek amendment 2 cell mismatch')
    if models.get('protocol_amendment')!=2: failures.append('active model config is not amendment 2')
    if failures:
        print('\n'.join(failures)); raise SystemExit('PROTOCOL AMENDMENT 2 VERIFICATION: FAIL')
    print('PROTOCOL AMENDMENT 2 VERIFICATION: PASS')
    print('amendment_fingerprint_sha256:',fp['amendment_fingerprint_sha256'])
    print('prompts_per_model:',len(manifest),'models:',len(models['models']),'planned_calls:',len(manifest)*len(models['models']))


if __name__=='__main__': main()
