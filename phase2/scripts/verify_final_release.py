from pathlib import Path
import gzip, hashlib, json
ROOT=Path(__file__).resolve().parents[1]

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    failures=[]
    pv=ROOT/'results/PRIMARY_VERIFICATION.json'
    if not pv.exists(): failures.append('missing primary verification')
    else:
        data=json.loads(pv.read_text())
        if data.get('status')!='PASS' or data.get('rows')!=8256: failures.append('primary verification not PASS/8256')
    for name in ['study_fingerprint.json','amendment3_fingerprint.json','amendment4_fingerprint.json','amendment5_fingerprint.json','robustness_fingerprint.json']:
        if not (ROOT/'freeze'/name).exists(): failures.append(f'missing freeze/{name}')
    figs=list((ROOT/'results/figures').glob('*.png'))
    if len(figs)<8: failures.append(f'expected at least 8 primary figures, found {len(figs)}')
    release=ROOT/'results/release/RELEASE_MANIFEST.json'
    if not release.exists(): failures.append('missing release manifest')
    else:
        m=json.loads(release.read_text())
        for e in m.get('files',[]):
            p=ROOT/e['path']
            if not p.exists(): failures.append(f"missing release file {e['path']}")
            elif sha256(p)!=e['sha256']: failures.append(f"sha mismatch {e['path']}")
        raw=[e for e in m.get('files',[]) if e['path'].startswith('results/release/raw/') and not 'robustness-' in e['path']]
        if len(raw)!=8: failures.append(f'expected 8 primary compressed raw ledgers, found {len(raw)}')
        for e in raw:
            p=ROOT/e['path']; rows=sum(1 for line in gzip.open(p,'rt',encoding='utf-8') if line.strip())
            if rows!=1032: failures.append(f"{e['path']} rows {rows} != 1032")
    paper=ROOT/'paper/main.tex'
    if not paper.exists(): failures.append('missing paper/main.tex')
    if failures:
        print('\n'.join(failures)); raise SystemExit('FINAL RELEASE VERIFICATION: FAIL')
    print('FINAL RELEASE VERIFICATION: PASS')
    print('primary_rows: 8256')
    print('primary_figures:',len(figs))
    print('release_manifest_sha256:',sha256(release))

if __name__=='__main__': main()
