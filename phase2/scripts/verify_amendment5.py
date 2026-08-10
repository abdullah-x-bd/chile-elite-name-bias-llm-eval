from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]

def blob(path):
    data=path.read_bytes(); return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()

def main():
    fp=json.loads((ROOT/'freeze/amendment5_fingerprint.json').read_text(encoding='utf-8'))
    failures=[]
    if fp.get('scientific_response_values_inspected') is not False: failures.append('amendment not outcome blind')
    if fp.get('scientific_settings_changed') is not False: failures.append('scientific settings unexpectedly changed')
    for rel,expected in fp['file_hashes'].items():
        p=ROOT/rel
        if not p.exists(): failures.append(f'missing {rel}'); continue
        got=blob(p)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    if failures:
        print('\n'.join(failures)); raise SystemExit('AMENDMENT 5 VERIFICATION: FAIL')
    print('AMENDMENT 5 VERIFICATION: PASS')
    print('amendment_fingerprint_sha256:',fp['amendment_fingerprint_sha256'])
    print('affected_cell:',fp['affected_cell'])
if __name__=='__main__': main()
