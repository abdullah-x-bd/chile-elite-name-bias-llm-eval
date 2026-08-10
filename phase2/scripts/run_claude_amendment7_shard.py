from pathlib import Path
import argparse, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.execution_amendment7 import CLAUDE_MAX_TOKENS, CLAUDE_REASONING, run_claude_amendment7
from chile_phase2.openrouter import request_identity, verify_frozen_models


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--shard-index',type=int,required=True)
    ap.add_argument('--shard-count',type=int,default=8)
    ap.add_argument('--cap-usd',type=float,required=True)
    args=ap.parse_args()
    if not 0<=args.shard_index<args.shard_count: raise ValueError('invalid shard index')
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='claude_sonnet5')
    verify_frozen_models({'models':[model]},verify_providers=True)
    full=load_manifest(ROOT)
    manifest=[p for i,p in enumerate(full) if i%args.shard_count==args.shard_index]
    expected=(len(full)+args.shard_count-1-args.shard_index)//args.shard_count
    if len(manifest)!=expected: raise RuntimeError('deterministic shard count mismatch')
    outdir=ROOT/'results/raw'; outdir.mkdir(parents=True,exist_ok=True)
    out=outdir/f'claude_sonnet5_a7_shard{args.shard_index:02d}.jsonl'; cumulative=0.0; done=set()
    if out.exists():
        for line in out.read_text(encoding='utf-8').splitlines():
            if line.strip():
                row=json.loads(line); done.add(row['request_identity']); cumulative+=float(row.get('cost_usd') or 0)
    with out.open('a',encoding='utf-8') as f:
        for local_idx,prompt in enumerate(manifest,1):
            payload=amended_request_payload(model,prompt,study); payload['max_tokens']=CLAUDE_MAX_TOKENS; payload['reasoning']=CLAUDE_REASONING
            rid=request_identity(study['study_id']+'::amendment7::claude-explicit-no-reasoning-160',model,prompt,payload)
            if rid in done: continue
            if cumulative+study['budget']['per_call_safety_allowance_usd']>args.cap_usd:
                raise RuntimeError(f'Claude Amendment 7 shard cap would be exceeded: shard={args.shard_index} cost=${cumulative:.4f} cap=${args.cap_usd:.2f}')
            result=run_claude_amendment7(model,prompt,study,cumulative,max_retries=5)
            cumulative+=float(result.get('cost_usd') or 0)
            if cumulative>args.cap_usd: raise RuntimeError('Claude Amendment 7 shard cap exceeded')
            f.write(json.dumps(result,ensure_ascii=False,sort_keys=True)+'\n'); f.flush()
            if local_idx%20==0 or local_idx==len(manifest): print('claude7_shard',args.shard_index,local_idx,'/',len(manifest),f'cost=${cumulative:.4f}')
    rows=[json.loads(x) for x in out.read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(rows)!=len(manifest): raise RuntimeError(f'incomplete shard {args.shard_index}: {len(rows)} != {len(manifest)}')
    if any(r.get('parse_status')!='ok' for r in rows): raise RuntimeError(f'semantic-invalid row in Claude Amendment 7 shard {args.shard_index}')
    expected_ids={p['prompt_id'] for p in manifest}
    if {r['prompt_id'] for r in rows}!=expected_ids: raise RuntimeError('shard prompt-id set mismatch')
    print('CLAUDE AMENDMENT 7 SHARD COMPLETE',args.shard_index,'rows=',len(rows),f'cost=${cumulative:.4f}')

if __name__=='__main__': main()
