from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest


def git_blob_sha1(path):
    data=path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def main():
    fp=json.loads((ROOT/'freeze/amendment3_fingerprint.json').read_text(encoding='utf-8'))
    if fp.get('scientific_response_values_inspected') is not False:
        raise SystemExit('FAIL: amendment 3 was not outcome-blind')
    failures=[]
    for rel,expected in fp['file_hashes'].items():
        path=ROOT/rel
        if not path.exists(): failures.append(f'missing {rel}'); continue
        got=git_blob_sha1(path)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    manifest=load_manifest(ROOT)
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    if len(manifest)!=fp['expected_prompts_per_model']: failures.append('manifest count mismatch')
    if len(cfg['models'])!=fp['expected_models']: failures.append('model count mismatch')
    if cfg.get('protocol_amendment')!=3: failures.append('active model config is not amendment 3')
    claude=[m for m in cfg['models'] if m['label']=='claude_sonnet5']
    if len(claude)!=1 or claude[0]['provider']!='anthropic' or claude[0]['reasoning']!='omit':
        failures.append('Claude amendment 3 cell mismatch')
    if failures:
        print('\n'.join(failures)); raise SystemExit('PROTOCOL AMENDMENT 3 VERIFICATION: FAIL')
    print('PROTOCOL AMENDMENT 3 VERIFICATION: PASS')
    print('amendment_fingerprint_sha256:',fp['amendment_fingerprint_sha256'])
    print('prompts_per_model:',len(manifest),'models:',len(cfg['models']),'planned_calls:',len(manifest)*len(cfg['models']))


if __name__=='__main__': main()
