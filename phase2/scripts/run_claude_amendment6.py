from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.execution_amendment6 import CLAUDE_MAX_TOKENS, run_claude_amendment6
from chile_phase2.openrouter import request_identity, verify_frozen_models

CAP_USD=2.70


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='claude_sonnet5')
    if model.get('reasoning')!='omit': raise RuntimeError('Claude reasoning must remain omitted under Amendment 6')
    verify_frozen_models({'models':[model]},verify_providers=True)
    manifest=load_manifest(ROOT)
    outdir=ROOT/'results/raw'; outdir.mkdir(parents=True,exist_ok=True)
    out=outdir/'claude_sonnet5.jsonl'; cumulative=0.0; done=set()
    if out.exists():
        for line in out.read_text(encoding='utf-8').splitlines():
            if line.strip():
                row=json.loads(line); done.add(row['request_identity']); cumulative+=float(row.get('cost_usd') or 0)
    with out.open('a',encoding='utf-8') as f:
        for idx,prompt in enumerate(manifest,1):
            payload=amended_request_payload(model,prompt,study); payload['max_tokens']=CLAUDE_MAX_TOKENS
            rid=request_identity(study['study_id']+'::amendment6::claude-160',model,prompt,payload)
            if rid in done: continue
            if cumulative+study['budget']['per_call_safety_allowance_usd']>CAP_USD:
                raise RuntimeError(f'Claude Amendment 6 cap would be exceeded: ${cumulative:.4f}/${CAP_USD:.2f}')
            result=run_claude_amendment6(model,prompt,study,cumulative,max_retries=5)
            cumulative+=float(result.get('cost_usd') or 0)
            if cumulative>CAP_USD: raise RuntimeError('Claude Amendment 6 cap exceeded')
            f.write(json.dumps(result,ensure_ascii=False,sort_keys=True)+'\n'); f.flush()
            if idx%25==0 or idx==len(manifest): print('claude_amendment6',idx,'/',len(manifest),f'cost=${cumulative:.4f}')
    rows=[json.loads(x) for x in out.read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(rows)!=len(manifest): raise RuntimeError(f'Incomplete Claude Amendment 6: {len(rows)} != {len(manifest)}')
    if any(r.get('parse_status')!='ok' for r in rows): raise RuntimeError('Claude Amendment 6 contains semantic-invalid rows')
    print('CLAUDE AMENDMENT 6 COMPLETE',len(rows),'rows',f'cost=${cumulative:.4f}')

if __name__=='__main__': main()
