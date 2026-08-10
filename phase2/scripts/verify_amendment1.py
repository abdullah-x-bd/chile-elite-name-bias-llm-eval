from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest


def git_blob_sha1(path):
    data=path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def main():
    fp=json.loads((ROOT/'freeze/amendment1_fingerprint.json').read_text(encoding='utf-8'))
    if fp.get('scientific_calls_started') is not False: raise SystemExit('FAIL: amendment not pre-outcome')
    failures=[]
    for rel,expected in fp['file_hashes'].items():
        path=ROOT/rel
        if not path.exists(): failures.append(f'missing {rel}'); continue
        got=git_blob_sha1(path)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    manifest=load_manifest(ROOT)
    if len(manifest)!=fp['expected_prompts_per_model']: failures.append('manifest count mismatch')
    models=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    if len(models['models'])!=fp['expected_models']: failures.append('model count mismatch')
    if any(m['label']=='deepseek_v4_flash' for m in models['models']): failures.append('superseded DeepSeek V4 cell still active')
    if not any(m['label']=='deepseek_v32' and m['provider']=='deepinfra' for m in models['models']): failures.append('amended DeepSeek V3.2/DeepInfra cell missing')
    if failures:
        print('\n'.join(failures)); raise SystemExit('PROTOCOL AMENDMENT 1 VERIFICATION: FAIL')
    print('PROTOCOL AMENDMENT 1 VERIFICATION: PASS')
    print('amendment_fingerprint_sha256:',fp['amendment_fingerprint_sha256'])
    print('prompts_per_model:',len(manifest),'models:',len(models['models']),'planned_calls:',len(manifest)*len(models['models']))


if __name__=='__main__': main()
