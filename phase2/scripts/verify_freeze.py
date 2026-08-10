from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

def git_blob_sha1(path: Path) -> str:
    data=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def main():
    fp=json.loads((ROOT/'freeze/study_fingerprint.json').read_text(encoding='utf-8'))
    if fp.get('scientific_calls_started') is not False: raise SystemExit('FAIL: fingerprint not pre-outcome')
    failures=[]
    for rel,expected in fp['file_hashes'].items():
        path=ROOT/rel
        if not path.exists(): failures.append(f'missing {rel}'); continue
        got=git_blob_sha1(path)
        if got!=expected: failures.append(f'git blob mismatch {rel}: {got} != {expected}')
    if failures:
        print('\n'.join(failures)); raise SystemExit('FAIL: freeze integrity')
    fp_base={k:v for k,v in fp.items() if k!='study_fingerprint_sha256'}
    recalculated=hashlib.sha256(json.dumps(fp_base,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if recalculated!=fp['study_fingerprint_sha256']: raise SystemExit('FAIL: study fingerprint mismatch')
    core=__import__('chile_phase2.core',fromlist=['load_manifest','load_jsonl'])
    manifest=core.load_manifest(ROOT)
    profiles=core.load_jsonl(ROOT/'data/frozen/base_profiles_v1.jsonl.gz.b64')
    if len(manifest)!=1032 or len(profiles)!=192: raise SystemExit('FAIL: frozen counts')
    if core.manifest_digest(manifest)!=fp['manifest_digest']: raise SystemExit('FAIL: manifest digest differs from fingerprint')
    print('PHASE II FREEZE VERIFICATION: PASS')
    print('study_fingerprint_sha256:',fp['study_fingerprint_sha256'])
    print('profiles:',len(profiles),'prompts_per_model:',len(manifest),'planned_calls:',len(manifest)*fp['expected_models'])
if __name__=='__main__': main()
