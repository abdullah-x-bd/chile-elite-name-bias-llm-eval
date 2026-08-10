from pathlib import Path
import copy, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.robustness import deterministic_subset
from chile_phase2.robustness_execution import run_robustness
from chile_phase2.openrouter import verify_frozen_models

CAP_USD=0.03


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    base=next(m for m in cfg['models'] if m['label']=='deepseek_v32')
    model=copy.deepcopy(base); model['label']='deepseek_v32_streamlake'; model['provider']='streamlake'
    verify_frozen_models({'models':[model]},verify_providers=True)
    subset=deterministic_subset(ROOT)
    outdir=ROOT/'results/robustness/raw'; outdir.mkdir(parents=True,exist_ok=True); out=outdir/'deepseek_v32_streamlake.jsonl'
    cost=0.0; done=set()
    if out.exists():
        for line in out.read_text(encoding='utf-8').splitlines():
            if line.strip():
                r=json.loads(line); done.add(r.get('source_prompt_id')); cost+=float(r.get('cost_usd') or 0)
    with out.open('a',encoding='utf-8') as f:
        for i,prompt in enumerate(subset,1):
            if prompt['prompt_id'] in done: continue
            if cost+0.01>CAP_USD: raise RuntimeError('Provider-sensitivity cap would be exceeded')
            r=run_robustness(model,prompt,study,'provider_sensitivity',1,cost,max_retries=4)
            cost+=float(r.get('cost_usd') or 0); f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n'); f.flush()
            if i%10==0 or i==len(subset): print('provider_sensitivity',i,'/',len(subset),f'cost=${cost:.4f}')
    rows=[json.loads(x) for x in out.read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(rows)!=52: raise RuntimeError(f'Provider sensitivity rows {len(rows)} != 52')
    print('PROVIDER SENSITIVITY COMPLETE',len(rows),'rows',f'cost=${cost:.4f}')

if __name__=='__main__': main()
