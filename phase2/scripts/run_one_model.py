from pathlib import Path
import argparse, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.execution_amendment2 import run_exact_amendment2
from chile_phase2.openrouter import request_identity, verify_frozen_models


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--label',required=True)
    ap.add_argument('--cap-usd',required=True,type=float)
    args=ap.parse_args()
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']==args.label)
    verify_frozen_models({'models':[model]},verify_providers=True)
    manifest=load_manifest(ROOT)
    outdir=ROOT/'results/raw'; outdir.mkdir(parents=True,exist_ok=True)
    out=outdir/f"{args.label}.jsonl"
    done=set(); cumulative=0.0
    if out.exists():
        for line in out.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            row=json.loads(line); done.add(row['request_identity']); cumulative += float(row.get('cost_usd') or 0)
    with out.open('a',encoding='utf-8') as f:
        for idx,prompt in enumerate(manifest,1):
            payload=amended_request_payload(model,prompt,study)
            rid=request_identity(study['study_id']+'::amendment2',model,prompt,payload)
            if rid in done: continue
            if cumulative + study['budget']['per_call_safety_allowance_usd'] > args.cap_usd:
                raise RuntimeError(f"Per-model budget cap would be exceeded for {args.label}: ${cumulative:.4f} / ${args.cap_usd:.4f}")
            result=run_exact_amendment2(model,prompt,study,cumulative,max_retries=5)
            cumulative += float(result.get('cost_usd') or 0)
            if cumulative > args.cap_usd:
                raise RuntimeError(f"Per-model budget cap exceeded after response for {args.label}: ${cumulative:.4f} / ${args.cap_usd:.4f}")
            f.write(json.dumps(result,ensure_ascii=False,sort_keys=True)+'\n'); f.flush()
            if idx % 25 == 0 or idx==len(manifest):
                print(args.label,idx,'/',len(manifest),f"cost=${cumulative:.4f}")
    rows=[json.loads(x) for x in out.read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(rows)!=len(manifest): raise RuntimeError(f"Incomplete model artifact {args.label}: {len(rows)} != {len(manifest)}")
    if len({r['request_identity'] for r in rows})!=len(rows): raise RuntimeError('Duplicate request identity')
    print('MODEL COMPLETE',args.label,'rows=',len(rows),'actual_cost=',round(cumulative,6))


if __name__=='__main__': main()
