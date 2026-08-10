from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]


def blob_sha(path):
    data=path.read_bytes(); return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def main():
    fp=json.loads((ROOT/'freeze/amendment6_fingerprint.json').read_text(encoding='utf-8'))
    failures=[]
    if fp.get('scientific_response_values_inspected') is not False: failures.append('Amendment 6 is not outcome blind')
    if fp.get('scientific_prompt_changed') is not False: failures.append('Scientific prompt changed unexpectedly')
    if fp.get('old_max_tokens')!=80 or fp.get('new_max_tokens')!=160: failures.append('Claude token amendment mismatch')
    for rel,expected in fp['file_hashes'].items():
        path=ROOT/rel
        if not path.exists(): failures.append(f'missing {rel}'); continue
        got=blob_sha(path)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    if failures:
        print('\n'.join(failures)); raise SystemExit('AMENDMENT 6 VERIFICATION: FAIL')
    print('AMENDMENT 6 VERIFICATION: PASS')
    print('amendment_fingerprint_sha256:',fp['amendment_fingerprint_sha256'])
    print('affected_cell:',fp['affected_cell'],'new_max_tokens:',fp['new_max_tokens'])

if __name__=='__main__': main()
