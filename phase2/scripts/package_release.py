from pathlib import Path
import gzip, hashlib, json, shutil
ROOT=Path(__file__).resolve().parents[1]


def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def deterministic_gzip(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    with src.open('rb') as inf, dst.open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as out:
            shutil.copyfileobj(inf,out)


def main():
    results=ROOT/'results'; release=results/'release'; rawrel=release/'raw'
    release.mkdir(parents=True,exist_ok=True); rawrel.mkdir(parents=True,exist_ok=True)
    model_cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    files=[]
    for m in model_cfg['models']:
        src=results/'raw'/f"{m['label']}.jsonl"
        if not src.exists(): raise RuntimeError(f'missing raw model ledger {src}')
        dst=rawrel/f"{m['label']}.jsonl.gz"; deterministic_gzip(src,dst); files.append(dst)
    required=[
        results/'PRIMARY_VERIFICATION.json', results/'RESULTS.md', results/'derived_all_responses.csv',
        results/'tables/primary_association.csv', results/'tables/primary_decision_leakage.csv',
        results/'tables/secondary_contrasts.csv', results/'tables/abstention_behavior.csv',
        results/'tables/task_competence.csv', results/'tables/surname_pair_coupling.csv',
        results/'tables/cost_ledger.csv', results/'statistics/summary.json', results/'statistics/coupling.json',
        results/'statistics/mixed_effects.txt'
    ]
    required += sorted((results/'figures').glob('*.png'))
    for p in required:
        if not p.exists(): raise RuntimeError(f'missing release result {p}')
        files.append(p)
    robust=results/'robustness'
    if robust.exists():
        files += sorted(p for p in robust.rglob('*') if p.is_file() and '/raw/' not in p.as_posix())
        for src in sorted((robust/'raw').glob('*.jsonl')):
            dst=rawrel/f"robustness-{src.stem}.jsonl.gz"; deterministic_gzip(src,dst); files.append(dst)
    entries=[]
    for p in sorted(set(files),key=lambda x:x.as_posix()):
        entries.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha256(p)})
    manifest={
        'release':'chile-phase2-v1.0.0',
        'phase1_commit':'feceba1fabbc8ba74d0bc55ca0ed6317a3a44bf0',
        'phase2_protocol_fingerprint':'46a83c263749b01e430e85a04241c800e2303d35093c146f55498b41aa1f02f0',
        'manifest_digest':'280bf06a20a2a3d346340a1d22d4496027c1cda574601121685fc0e37efdb2ff',
        'amendment3_fingerprint':'5df71914a146dc4b8ee23163031c4875b94c281d7d5143b5391e0704d3c5e9ec',
        'amendment4_fingerprint':'afda642c2167c63bd56b6087884181842bdc00bb924d2a1b5d8b65773c86eb01',
        'amendment5_fingerprint':'b00b1298529e57bce01f313177a57715aa4c04c66368cd0a46aac06a4e2598af',
        'robustness_fingerprint':'2709d483c8c85fc7f56539eb4e98373d2d0b3988f244e37bfe5eb55c76455062',
        'files':entries,
    }
    manifest_path=release/'RELEASE_MANIFEST.json'
    manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('RELEASE PACKAGE BUILT',len(entries),'files')
    print('manifest_sha256',sha256(manifest_path))

if __name__=='__main__': main()
