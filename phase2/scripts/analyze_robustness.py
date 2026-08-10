from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
from chile_phase2.core import load_manifest


def scalar(prompt,parsed):
    if prompt['bank']=='association':
        if prompt['domain']=='university_prestige': return parsed.get('high_prestige')
        return parsed.get('private_paid')
    return parsed.get('score')

def categorical(prompt,parsed):
    if prompt['bank']=='association' and prompt['instrument'].endswith('_abstention'): return parsed.get('can_infer')
    if prompt['bank']!='association': return parsed.get('recommendation')
    return None


def main():
    primary_dir=ROOT/'results/raw'; robust_dir=ROOT/'results/robustness/raw'; out=ROOT/'results/robustness'
    out.mkdir(parents=True,exist_ok=True)
    manifest={r['prompt_id']:r for r in load_manifest(ROOT)}
    primary={}
    for fp in primary_dir.glob('*.jsonl'):
        if fp.parent==robust_dir: continue
        for line in fp.read_text(encoding='utf-8').splitlines():
            if line.strip():
                r=json.loads(line); primary[(fp.stem,r['prompt_id'])]=r
    robust=[]
    for fp in robust_dir.glob('*.jsonl'):
        for line in fp.read_text(encoding='utf-8').splitlines():
            if line.strip():
                r=json.loads(line); r['artifact_label']=fp.stem; robust.append(r)
    rdf=pd.DataFrame(robust)
    if len(rdf)!=1300: raise RuntimeError(f'Robustness rows {len(rdf)} != 1300')
    summaries=[]
    # Stability: rep1 vs rep2 and both vs primary.
    for model,g in rdf[rdf.robustness_family=='stability'].groupby('artifact_label'):
        rows={}
        for r in g.to_dict('records'):
            src=r['source_prompt_id']; prompt=manifest[src]; rows[(src,int(r['replicate']))]=(scalar(prompt,r['parsed_response']),categorical(prompt,r['parsed_response']))
        numeric=[]; agreements=[]; primary_abs=[]
        for src in sorted({k[0] for k in rows}):
            a,ca=rows[(src,1)]; b,cb=rows[(src,2)]; prompt=manifest[src]
            if a is not None and b is not None: numeric.append(abs(float(a)-float(b)))
            if ca is not None and cb is not None: agreements.append(ca==cb)
            pr=primary.get((model,src))
            if pr is not None:
                pv=scalar(prompt,pr['parsed_response'])
                for v in (a,b):
                    if v is not None and pv is not None: primary_abs.append(abs(float(v)-float(pv)))
        summaries.append({'family':'stability','model_label':model,'n_prompts':52,'mean_abs_rep1_rep2':float(np.mean(numeric)) if numeric else None,'categorical_agreement':float(np.mean(agreements)) if agreements else None,'mean_abs_repeat_vs_primary':float(np.mean(primary_abs)) if primary_abs else None})
    # English vs Spanish primary.
    for model,g in rdf[rdf.robustness_family=='english'].groupby('artifact_label'):
        diffs=[]; absdiff=[]; agree=[]
        for r in g.to_dict('records'):
            src=r['source_prompt_id']; prompt=manifest[src]; pr=primary.get((model,src))
            if pr is None: continue
            ev=scalar(prompt,r['parsed_response']); sv=scalar(prompt,pr['parsed_response'])
            if ev is not None and sv is not None: diffs.append(float(ev)-float(sv)); absdiff.append(abs(float(ev)-float(sv)))
            ec=categorical(prompt,r['parsed_response']); sc=categorical(prompt,pr['parsed_response'])
            if ec is not None and sc is not None: agree.append(ec==sc)
        summaries.append({'family':'english_context_shift','model_label':model,'n_prompts':52,'mean_signed_shift':float(np.mean(diffs)) if diffs else None,'mean_absolute_shift':float(np.mean(absdiff)) if absdiff else None,'categorical_agreement':float(np.mean(agree)) if agree else None})
    # DeepSeek provider sensitivity vs primary DeepInfra.
    g=rdf[rdf.robustness_family=='provider_sensitivity']
    diffs=[]; absdiff=[]; agree=[]
    for r in g.to_dict('records'):
        src=r['source_prompt_id']; prompt=manifest[src]; pr=primary.get(('deepseek_v32',src))
        if pr is None: continue
        av=scalar(prompt,r['parsed_response']); bv=scalar(prompt,pr['parsed_response'])
        if av is not None and bv is not None: diffs.append(float(av)-float(bv)); absdiff.append(abs(float(av)-float(bv)))
        ac=categorical(prompt,r['parsed_response']); bc=categorical(prompt,pr['parsed_response'])
        if ac is not None and bc is not None: agree.append(ac==bc)
    summaries.append({'family':'provider_sensitivity','model_label':'deepseek_v32_streamlake_vs_deepinfra','n_prompts':52,'mean_signed_shift':float(np.mean(diffs)) if diffs else None,'mean_absolute_shift':float(np.mean(absdiff)) if absdiff else None,'categorical_agreement':float(np.mean(agree)) if agree else None})
    summary=pd.DataFrame(summaries); summary.to_csv(out/'ROBUSTNESS_SUMMARY.csv',index=False)
    total_cost=float(rdf.cost_usd.fillna(0).sum())
    obj={'rows':len(rdf),'total_cost_usd':total_cost,'families':summary.to_dict('records')}
    (out/'ROBUSTNESS_SUMMARY.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines=['# Phase II robustness results','',f'Robustness calls analyzed: **{len(rdf):,}**.',f'Recorded robustness-call cost: **${total_cost:.4f}**.','','These analyses were predeclared as secondary and are not pooled into the four primary confirmatory estimands.','']
    for row in summaries:
        lines.append(f"## {row['family']} | {row['model_label']}")
        for k,v in row.items():
            if k not in {'family','model_label'}: lines.append(f'- {k}: {v}')
        lines.append('')
    (out/'ROBUSTNESS_RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(obj,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
