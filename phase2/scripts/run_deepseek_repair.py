from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.execution_amendment3 import run_exact_amendment3
from chile_phase2.openrouter import request_identity, verify_frozen_models

CAP_USD=0.08


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='deepseek_v32')
    verify_frozen_models({'models':[model]},verify_providers=True)
    manifest=load_manifest(ROOT)
    outdir=ROOT/'results/raw'; outdir.mkdir(parents=True,exist_ok=True)
    out=outdir/'deepseek_v32.jsonl'; cumulative=0.0; done=set()
    if out.exists():
        for line in out.read_text(encoding='utf-8').splitlines():
            if line.strip():
                row=json.loads(line); done.add(row['request_identity']); cumulative += float(row.get('cost_usd') or 0)
    with out.open('a',encoding='utf-8') as f:
        for idx,prompt in enumerate(manifest,1):
            payload=amended_request_payload(model,prompt,study)
            rid=request_identity(study['study_id']+'::amendment5::deepseek-repair',model,prompt,payload)
            if rid in done: continue
            if cumulative + study['budget']['per_call_safety_allowance_usd'] > CAP_USD:
                raise RuntimeError(f'DeepSeek repair cap would be exceeded: ${cumulative:.4f}/${CAP_USD:.4f}')
            result=run_exact_amendment3(model,prompt,study,cumulative,max_retries=5)
            result['request_identity']=rid; result['protocol_amendment']=5
            cumulative += float(result.get('cost_usd') or 0)
            if cumulative > CAP_USD: raise RuntimeError('DeepSeek repair cap exceeded')
            f.write(json.dumps(result,ensure_ascii=False,sort_keys=True)+'\n'); f.flush()
            if idx%25==0 or idx==len(manifest): print('deepseek_repair',idx,'/',len(manifest),f'cost=${cumulative:.4f}')
    rows=[json.loads(x) for x in out.read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(rows)!=len(manifest): raise RuntimeError(f'Incomplete DeepSeek repair: {len(rows)} != {len(manifest)}')
    print('DEEPSEEK REPAIR COMPLETE',len(rows),'rows',f'cost=${cumulative:.4f}')

if __name__=='__main__': main()
