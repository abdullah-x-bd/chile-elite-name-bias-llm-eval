from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]


def blob_sha(path):
    data=path.read_bytes(); return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def main():
    fp=json.loads((ROOT/'freeze/amendment9_fingerprint.json').read_text(encoding='utf-8'))
    failures=[]
    if fp.get('scientific_response_values_inspected') is not False: failures.append('Amendment 9 is not outcome blind')
    if fp.get('scientific_prompt_changed') is not False: failures.append('Scientific prompt changed unexpectedly')
    if fp.get('affected_cell')!='mistral_medium35': failures.append('Affected model mismatch')
    if fp.get('affected_prompt_id')!='assoc::common_frequency::flores::school_sector::1': failures.append('Affected prompt mismatch')
    if fp.get('semantic_invalid_policy')!='retry_identical_request_up_to_existing_retry_limit': failures.append('Semantic retry policy mismatch')
    for rel,expected in fp['file_hashes'].items():
        path=ROOT/rel
        if not path.exists(): failures.append(f'missing {rel}'); continue
        got=blob_sha(path)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    payload={k:v for k,v in fp.items() if k!='amendment_fingerprint_sha256'}
    got_fp=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if got_fp!=fp.get('amendment_fingerprint_sha256'): failures.append(f'fingerprint mismatch {got_fp}')
    if failures:
        print('\n'.join(failures)); raise SystemExit('AMENDMENT 9 VERIFICATION: FAIL')
    print('AMENDMENT 9 VERIFICATION: PASS')
    print('amendment_fingerprint_sha256:',fp['amendment_fingerprint_sha256'])
    print('affected_prompt_id:',fp['affected_prompt_id'])

if __name__=='__main__': main()
