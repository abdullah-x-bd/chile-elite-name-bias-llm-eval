from pathlib import Path
import argparse, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.execution_amendment3 import run_exact_amendment3
from chile_phase2.openrouter import request_identity, verify_frozen_models


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--shard-index',type=int,required=True); ap.add_argument('--shard-count',type=int,default=4); ap.add_argument('--cap-usd',type=float,required=True); args=ap.parse_args()
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8')); cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='deepseek_v32'); verify_frozen_models({'models':[model]},verify_providers=True)
    full=load_manifest(ROOT); manifest=[p for i,p in enumerate(full) if i%args.shard_count==args.shard_index]
    outdir=ROOT/'results/raw'; outdir.mkdir(parents=True,exist_ok=True); out=outdir/f'deepseek_v32_shard{args.shard_index:02d}.jsonl'; cost=0.0
    with out.open('w',encoding='utf-8') as f:
        for j,prompt in enumerate(manifest,1):
            payload=amended_request_payload(model,prompt,study); rid=request_identity(study['study_id']+'::amendment5::deepseek-repair',model,prompt,payload)
            if cost+study['budget']['per_call_safety_allowance_usd']>args.cap_usd: raise RuntimeError('DeepSeek shard cap would be exceeded')
            r=run_exact_amendment3(model,prompt,study,cost,max_retries=5); r['request_identity']=rid; r['protocol_amendment']=5; cost+=float(r.get('cost_usd') or 0)
            f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n'); f.flush()
            if j%40==0 or j==len(manifest): print('deepseek5_shard',args.shard_index,j,'/',len(manifest),f'cost=${cost:.4f}')
    rows=[json.loads(x) for x in out.read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(rows)!=len(manifest) or any(r.get('parse_status')!='ok' for r in rows): raise RuntimeError('DeepSeek shard validation failed')
    if {r['prompt_id'] for r in rows}!={p['prompt_id'] for p in manifest}: raise RuntimeError('DeepSeek shard prompt set mismatch')
    print('DEEPSEEK AMENDMENT 5 SHARD COMPLETE',args.shard_index,'rows=',len(rows),f'cost=${cost:.4f}')
if __name__=='__main__': main()
