from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.robustness import BANK_TARGETS, deterministic_subset, english_prompt


def blob_sha(path):
    data=path.read_bytes(); return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()

def digest(rows):
    payload=''.join(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n' for r in rows)
    return hashlib.sha256(payload.encode()).hexdigest()


def main():
    fp=json.loads((ROOT/'freeze/robustness_fingerprint.json').read_text(encoding='utf-8'))
    if fp.get('outcome_blind') is not True: raise SystemExit('ROBUSTNESS FREEZE FAIL: not outcome blind')
    failures=[]
    for rel,expected in fp['file_hashes'].items():
        p=ROOT/rel
        if not p.exists(): failures.append(f'missing {rel}'); continue
        got=blob_sha(p)
        if got!=expected: failures.append(f'hash mismatch {rel}: {got} != {expected}')
    subset=deterministic_subset(ROOT); english=[english_prompt(ROOT,r) for r in subset]
    compact=[{'prompt_id':r['prompt_id'],'bank':r['bank'],'prompt_sha256':r['prompt_sha256']} for r in subset]
    compact_en=[{'prompt_id':r['prompt_id'],'bank':r['bank'],'prompt_sha256':r['prompt_sha256']} for r in english]
    if len(subset)!=52: failures.append('subset count mismatch')
    if {b:sum(r['bank']==b for r in subset) for b in BANK_TARGETS}!=BANK_TARGETS: failures.append('bank allocation mismatch')
    if digest(compact)!=fp['spanish_subset_digest_sha256']: failures.append('Spanish subset digest mismatch')
    if digest(compact_en)!=fp['english_subset_digest_sha256']: failures.append('English subset digest mismatch')
    if failures:
        print('\n'.join(failures)); raise SystemExit('ROBUSTNESS FREEZE VERIFICATION: FAIL')
    print('ROBUSTNESS FREEZE VERIFICATION: PASS')
    print('robustness_fingerprint_sha256:',fp['robustness_fingerprint_sha256'])
    print('spanish_subset_digest:',fp['spanish_subset_digest_sha256'])
    print('english_subset_digest:',fp['english_subset_digest_sha256'])
    print('planned_calls:',fp['planned_calls']['total'])

if __name__=='__main__': main()
