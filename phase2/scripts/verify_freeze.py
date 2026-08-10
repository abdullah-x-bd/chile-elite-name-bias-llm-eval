from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    fp=json.loads((ROOT/'freeze/study_fingerprint.json').read_text())
    if fp.get('scientific_calls_started') is not False: raise SystemExit('FAIL: fingerprint not pre-outcome')
    failures=[]
    for rel,expected in fp['file_hashes'].items():
        path=ROOT/rel
        if not path.exists(): failures.append(f'missing {rel}'); continue
        got=sha(path)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    if failures:
        print('\n'.join(failures)); raise SystemExit('FAIL: freeze integrity')
    manifest=sum(1 for x in __import__('gzip').decompress(__import__('base64').b64decode((ROOT/'data/frozen/prompt_manifest_v1.jsonl.gz.b64').read_text(encoding='ascii'))).decode('utf-8').splitlines() if x.strip())
    profiles=sum(1 for x in (ROOT/'data/frozen/base_profiles_v1.jsonl').read_text(encoding='utf-8').splitlines() if x.strip())
    if manifest!=1032 or profiles!=192: raise SystemExit('FAIL: frozen counts')
    print('PHASE II FREEZE VERIFICATION: PASS')
    print('study_fingerprint_sha256:',fp['study_fingerprint_sha256'])
    print('profiles:',profiles,'prompts_per_model:',manifest,'planned_calls:',manifest*fp['expected_models'])
if __name__=='__main__': main()
