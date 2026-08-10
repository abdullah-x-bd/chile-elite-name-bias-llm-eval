from pathlib import Path
import base64, gzip, json, math, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from chile_phase2.core import load_manifest, load_jsonl, load_csv

SEED=20260810
rng=np.random.default_rng(SEED)


def bootstrap_diff(a,b,n=10000,paired=False):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float)
    vals=np.empty(n)
    if paired:
        d=a-b
        for i in range(n): vals[i]=rng.choice(d,size=len(d),replace=True).mean()
    else:
        for i in range(n): vals[i]=rng.choice(a,size=len(a),replace=True).mean()-rng.choice(b,size=len(b),replace=True).mean()
    return float(np.quantile(vals,.025)),float(np.quantile(vals,.975))


def bh_adjust(pvals):
    p=np.asarray(pvals,dtype=float); n=len(p); order=np.argsort(p); out=np.empty(n); running=1.0
    for rank_idx in range(n-1,-1,-1):
        idx=order[rank_idx]; rank=rank_idx+1; running=min(running,p[idx]*n/rank); out[idx]=min(1.0,running)
    return out


def load_rows():
    manifest={r['prompt_id']:r for r in load_manifest(ROOT)}
    model_cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    request_to_label={m['request_id']:m['label'] for m in model_cfg['models']}
    rows=[]
    for fp in sorted((ROOT/'results/raw').glob('*.jsonl')):
        label=fp.stem
        for line in fp.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            raw=json.loads(line); meta=manifest[raw['prompt_id']]
            parsed=raw.get('parsed_response') or {}
            row={k:v for k,v in meta.items() if k not in ('schema','prompt_text')}
            row.update({'model_label':label,'requested_model':raw.get('requested_model'),'returned_model':raw.get('returned_model'),'requested_provider':raw.get('requested_provider'),'returned_provider':raw.get('returned_provider'),'parse_status':raw.get('parse_status'),'semantic_status':raw.get('semantic_status'),'cost_usd':float(raw.get('cost_usd') or 0),'latency_ms':float(raw.get('latency_ms') or 0),'retry_count':int(raw.get('retry_count') or 0),'finish_reason':raw.get('finish_reason')})
            if meta['bank']=='association':
                if meta['domain']=='university_prestige': row['high_status_mass']=parsed.get('high_prestige')
                else: row['high_status_mass']=parsed.get('private_paid')
                row['can_infer']=parsed.get('can_infer')
            else:
                row['score']=parsed.get('score'); row['recommendation']=parsed.get('recommendation'); row['confidence']=parsed.get('confidence')
            rows.append(row)
    return pd.DataFrame(rows), model_cfg


def paired_contrast(df,a,b):
    piv=df.pivot(index='base_profile_id',columns='condition',values='score').dropna(subset=[a,b])
    x=piv[a].astype(float).to_numpy(); y=piv[b].astype(float).to_numpy(); d=x-y
    mean=float(d.mean()); ci=bootstrap_diff(x,y,paired=True); t,p=stats.ttest_rel(x,y)
    return {'n':len(d),'mean_diff':mean,'ci_low':ci[0],'ci_high':ci[1],'t':float(t),'p':float(p),'diffs':d,'pivot':piv}


def main():
    out=ROOT/'results'; tables=out/'tables'; figs=out/'figures'; statsdir=out/'statistics'
    for d in (tables,figs,statsdir): d.mkdir(parents=True,exist_ok=True)
    df,model_cfg=load_rows()
    expected=1032*len(model_cfg['models'])
    if len(df)!=expected: raise RuntimeError(f'Expected {expected} raw rows, found {len(df)}')
    df.to_csv(out/'derived_all_responses.csv',index=False)
    valid=df[df['parse_status']=='ok'].copy()

    cost=(df.groupby(['model_label','requested_model','requested_provider'],dropna=False).agg(requests=('prompt_id','size'),cost_usd=('cost_usd','sum'),mean_latency_ms=('latency_ms','mean'),retries=('retry_count','sum')).reset_index())
    cost.to_csv(tables/'cost_ledger.csv',index=False)

    af=valid[(valid.bank=='association') & valid.instrument.str.endswith('_forced')].copy()
    surname_scores=(af.groupby(['model_label','surname','surname_group'],as_index=False).high_status_mass.mean().rename(columns={'high_status_mass':'association_score'}))
    surname_scores.to_csv(tables/'surname_model_association.csv',index=False)
    assoc_rows=[]
    for model,g in surname_scores.groupby('model_label'):
        e=g[g.surname_group=='elite_coded'].association_score.to_numpy(float)
        c=g[g.surname_group=='common_frequency'].association_score.to_numpy(float)
        r=g[g.surname_group=='rare_frequency'].association_score.to_numpy(float)
        for name,x,y in [('elite_minus_common',e,c),('elite_minus_rare',e,r)]:
            t,p=stats.ttest_ind(x,y,equal_var=False); ci=bootstrap_diff(x,y,paired=False)
            assoc_rows.append({'model_label':model,'contrast':name,'n_a':len(x),'n_b':len(y),'mean_a':x.mean(),'mean_b':y.mean(),'mean_diff':x.mean()-y.mean(),'ci_low':ci[0],'ci_high':ci[1],'t':t,'p':p})
    assoc=pd.DataFrame(assoc_rows); assoc.to_csv(tables/'primary_association.csv',index=False)

    dm=valid[valid.bank=='decision_main'].copy()
    leak_rows=[]; model_pivots={}
    for model,g in dm.groupby('model_label'):
        res=paired_contrast(g,'elite','common'); model_pivots[model]=res['pivot']
        blind=res['pivot']['blind'].astype(float).to_numpy(); sd=float(np.std(blind,ddof=1)); se=float(np.std(res['diffs'],ddof=1)/math.sqrt(len(res['diffs'])))
        margin=.10*sd
        if se>0:
            tlo=(res['mean_diff']-(-margin))/se; plo=1-stats.t.cdf(tlo,len(res['diffs'])-1)
            thi=(res['mean_diff']-margin)/se; phi=stats.t.cdf(thi,len(res['diffs'])-1)
        else:
            plo=0.0 if res['mean_diff']>-margin else 1.0; phi=0.0 if res['mean_diff']<margin else 1.0
        leak_rows.append({'model_label':model,'n':res['n'],'mean_diff':res['mean_diff'],'ci_low':res['ci_low'],'ci_high':res['ci_high'],'paired_t':res['t'],'p':res['p'],'blind_sd':sd,'standardized_effect':res['mean_diff']/sd if sd else np.nan,'equivalence_margin_points':margin,'tost_p_lower':plo,'tost_p_upper':phi,'equivalent_within_0_10_sd':bool(plo<.05 and phi<.05)})
    leakage=pd.DataFrame(leak_rows); leakage.to_csv(tables/'primary_decision_leakage.csv',index=False)

    secondary=[]
    for model,g in valid[valid.bank.isin(['decision_main','decision_rare','decision_metadata','decision_holistic'])].groupby('model_label'):
        main=g[g.bank=='decision_main']
        for a,b,label in [('elite','blind','main_elite_minus_blind'),('common','blind','main_common_minus_blind')]:
            res=paired_contrast(main,a,b); secondary.append({'model_label':model,'family':'main_secondary','contrast':label,'n':res['n'],'mean_diff':res['mean_diff'],'ci_low':res['ci_low'],'ci_high':res['ci_high'],'p':res['p']})
        rare=g[g.bank=='decision_rare'][['base_profile_id','score']].rename(columns={'score':'rare_score'})
        blind=main[main.condition=='blind'][['base_profile_id','score']].rename(columns={'score':'blind_score'})
        rr=rare.merge(blind,on='base_profile_id').dropna(); d=rr.rare_score.astype(float)-rr.blind_score.astype(float); t,p=stats.ttest_1samp(d,0); ci=bootstrap_diff(rr.rare_score,rr.blind_score,paired=True)
        secondary.append({'model_label':model,'family':'main_secondary','contrast':'rare_minus_blind','n':len(d),'mean_diff':d.mean(),'ci_low':ci[0],'ci_high':ci[1],'p':p})
        for bank,a,b,label in [('decision_metadata','elite_metadata','common_metadata','metadata_elite_minus_common'),('decision_holistic','elite','common','holistic_elite_minus_common')]:
            res=paired_contrast(g[g.bank==bank],a,b); secondary.append({'model_label':model,'family':bank,'contrast':label,'n':res['n'],'mean_diff':res['mean_diff'],'ci_low':res['ci_low'],'ci_high':res['ci_high'],'p':res['p']})
        for domain,dg in main.groupby('domain'):
            res=paired_contrast(dg,'elite','common'); secondary.append({'model_label':model,'family':'domain','contrast':f'{domain}_elite_minus_common','n':res['n'],'mean_diff':res['mean_diff'],'ci_low':res['ci_low'],'ci_high':res['ci_high'],'p':res['p']})
    sec=pd.DataFrame(secondary)
    sec['p_fdr']=np.nan
    for fam,idx in sec.groupby('family').groups.items(): sec.loc[idx,'p_fdr']=bh_adjust(sec.loc[idx,'p'].fillna(1).to_numpy())
    sec.to_csv(tables/'secondary_contrasts.csv',index=False)

    aa=valid[(valid.bank=='association') & valid.instrument.str.endswith('_abstention')].copy()
    abst=(aa.groupby(['model_label','surname_group','domain']).agg(n=('prompt_id','size'),infer_rate=('can_infer',lambda x: float(pd.Series(x).fillna(False).mean())),mean_high_status_mass=('high_status_mass','mean')).reset_index())
    abst.to_csv(tables/'abstention_behavior.csv',index=False)

    profiles=load_jsonl(ROOT/'data/frozen/base_profiles_v1.jsonl.gz.b64'); pmap={p['profile_id']:p for p in profiles}
    comp=[]
    blind_rows=dm[dm.condition=='blind'].copy(); blind_rows['normative_score']=blind_rows.base_profile_id.map(lambda x:pmap[x]['normative_score'])
    for model,g in blind_rows.groupby('model_label'):
        rho,p=stats.spearmanr(g.normative_score.astype(float),g.score.astype(float))
        comp.append({'model_label':model,'n':len(g),'spearman_rho':rho,'p':p,'mae_vs_normative':float(np.mean(np.abs(g.score.astype(float)-g.normative_score.astype(float))))})
    competence=pd.DataFrame(comp); competence.to_csv(tables/'task_competence.csv',index=False)

    aec=assoc[assoc.contrast=='elite_minus_common'][['model_label','mean_diff']].rename(columns={'mean_diff':'association_diff'})
    dl=leakage[['model_label','mean_diff']].rename(columns={'mean_diff':'leakage_diff'})
    mc=aec.merge(dl,on='model_label'); pr=stats.pearsonr(mc.association_diff,mc.leakage_diff); sr=stats.spearmanr(mc.association_diff,mc.leakage_diff)
    model_coupling={'pearson_r':float(pr.statistic),'pearson_p':float(pr.pvalue),'spearman_rho':float(sr.statistic),'spearman_p':float(sr.pvalue),'n_models':len(mc)}
    surnames=load_csv(ROOT/'data/frozen/surnames_v1.csv'); elite=[r['surname'] for r in surnames if r['group']=='elite_coded']; common=[r['surname'] for r in surnames if r['group']=='common_frequency']; pair_map=dict(zip(elite,common))
    pair_rows=[]
    for model in surname_scores.model_label.unique():
        sg=surname_scores[surname_scores.model_label==model].set_index('surname').association_score
        md=dm[dm.model_label==model]
        ep=md[md.condition=='elite'][['base_profile_id','surname','score']].rename(columns={'surname':'elite_surname','score':'elite_score'})
        cp=md[md.condition=='common'][['base_profile_id','surname','score']].rename(columns={'surname':'common_surname','score':'common_score'})
        z=ep.merge(cp,on='base_profile_id'); z['decision_diff']=z.elite_score.astype(float)-z.common_score.astype(float)
        for en,cn in pair_map.items():
            zz=z[(z.elite_surname==en)&(z.common_surname==cn)]
            if len(zz): pair_rows.append({'model_label':model,'elite_surname':en,'common_surname':cn,'association_diff':float(sg.get(en,np.nan)-sg.get(cn,np.nan)),'decision_diff':float(zz.decision_diff.mean()),'n_profiles':len(zz)})
    pairs=pd.DataFrame(pair_rows); pairs.to_csv(tables/'surname_pair_coupling.csv',index=False)
    ppr=stats.pearsonr(pairs.association_diff,pairs.decision_diff); psr=stats.spearmanr(pairs.association_diff,pairs.decision_diff)
    pair_coupling={'pearson_r':float(ppr.statistic),'pearson_p':float(ppr.pvalue),'spearman_rho':float(psr.statistic),'spearman_p':float(psr.pvalue),'n_cells':len(pairs)}
    (statsdir/'coupling.json').write_text(json.dumps({'model_level':model_coupling,'surname_pair_level':pair_coupling},indent=2),encoding='utf-8')

    mixed_status='not_run'
    try:
        import statsmodels.formula.api as smf
        md=dm[['score','condition','model_label','domain','base_profile_id']].dropna().copy(); md['score']=md.score.astype(float)
        fit=smf.mixedlm('score ~ C(condition) * C(model_label) + C(domain)',md,groups=md['base_profile_id']).fit(method='lbfgs',maxiter=500,disp=False)
        (statsdir/'mixed_effects.txt').write_text(str(fit.summary()),encoding='utf-8'); mixed_status='success'
    except Exception as exc:
        (statsdir/'mixed_effects.txt').write_text('Mixed-effects fit failed transparently:\n'+repr(exc),encoding='utf-8'); mixed_status='failed'

    order=[m['label'] for m in model_cfg['models']]
    def forest(table,path,title,xlabel):
        t=table.set_index('model_label').reindex(order).dropna(subset=['mean_diff']); y=np.arange(len(t)); x=t.mean_diff.to_numpy(float); lo=x-t.ci_low.to_numpy(float); hi=t.ci_high.to_numpy(float)-x
        fig,ax=plt.subplots(figsize=(8,5)); ax.errorbar(x,y,xerr=np.vstack([lo,hi]),fmt='o',capsize=3); ax.axvline(0,linewidth=1); ax.set_yticks(y,t.index); ax.set_xlabel(xlabel); ax.set_title(title); fig.tight_layout(); fig.savefig(path,dpi=180); plt.close(fig)
    forest(assoc[assoc.contrast=='elite_minus_common'],figs/'01_association_effect_by_model.png','Elite minus common latent association','High-status probability points')
    forest(leakage,figs/'02_decision_leakage_by_model.png','Elite minus common decision leakage','Decision-score points')
    fig,ax=plt.subplots(figsize=(7,5)); ax.scatter(mc.association_diff,mc.leakage_diff); [ax.annotate(r.model_label,(r.association_diff,r.leakage_diff),fontsize=8) for r in mc.itertuples()]; ax.axhline(0,linewidth=1); ax.axvline(0,linewidth=1); ax.set_xlabel('Elite-common association difference'); ax.set_ylabel('Elite-common decision leakage'); ax.set_title('Association versus decision leakage'); fig.tight_layout(); fig.savefig(figs/'03_association_vs_leakage.png',dpi=180); plt.close(fig)
    heat=surname_scores.pivot(index='model_label',columns='surname',values='association_score').reindex(order); fig,ax=plt.subplots(figsize=(14,5)); im=ax.imshow(heat.to_numpy(float),aspect='auto'); ax.set_yticks(range(len(heat.index)),heat.index); ax.set_xticks(range(len(heat.columns)),heat.columns,rotation=90,fontsize=7); ax.set_title('Forced high-status association by surname and model'); fig.colorbar(im,ax=ax,label='High-status mass'); fig.tight_layout(); fig.savefig(figs/'04_surname_model_heatmap.png',dpi=180); plt.close(fig)
    sh=sec[sec.contrast=='holistic_elite_minus_common'][['model_label','mean_diff']].rename(columns={'mean_diff':'holistic'}).merge(leakage[['model_label','mean_diff']].rename(columns={'mean_diff':'structured'}),on='model_label').set_index('model_label').reindex(order); fig,ax=plt.subplots(figsize=(9,5)); x=np.arange(len(sh)); w=.36; ax.bar(x-w/2,sh.structured,w,label='Structured'); ax.bar(x+w/2,sh.holistic,w,label='Holistic'); ax.axhline(0,linewidth=1); ax.set_xticks(x,sh.index,rotation=35,ha='right'); ax.set_ylabel('Elite-common score difference'); ax.set_title('Structured versus holistic leakage'); ax.legend(); fig.tight_layout(); fig.savefig(figs/'05_structured_vs_holistic.png',dpi=180); plt.close(fig)
    vm=sec[sec.contrast=='metadata_elite_minus_common'][['model_label','mean_diff']].rename(columns={'mean_diff':'metadata'}).merge(leakage[['model_label','mean_diff']].rename(columns={'mean_diff':'visible'}),on='model_label').set_index('model_label').reindex(order); fig,ax=plt.subplots(figsize=(9,5)); x=np.arange(len(vm)); ax.bar(x-w/2,vm.visible,w,label='Visible'); ax.bar(x+w/2,vm.metadata,w,label='Metadata-only'); ax.axhline(0,linewidth=1); ax.set_xticks(x,vm.index,rotation=35,ha='right'); ax.set_ylabel('Elite-common score difference'); ax.set_title('Visible versus metadata-only leakage'); ax.legend(); fig.tight_layout(); fig.savefig(figs/'06_visible_vs_metadata.png',dpi=180); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5)); groups=['elite_coded','common_frequency','rare_frequency']; data=[surname_scores[surname_scores.surname_group==g].association_score.to_numpy(float) for g in groups]; ax.boxplot(data,tick_labels=groups); ax.set_ylabel('High-status association score'); ax.set_title('Forced association distribution by surname group'); fig.tight_layout(); fig.savefig(figs/'07_association_group_distributions.png',dpi=180); plt.close(fig)
    cl=competence.merge(leakage[['model_label','mean_diff']].rename(columns={'mean_diff':'leakage_diff'}),on='model_label'); fig,ax=plt.subplots(figsize=(7,5)); ax.scatter(cl.spearman_rho,cl.leakage_diff); [ax.annotate(r.model_label,(r.spearman_rho,r.leakage_diff),fontsize=8) for r in cl.itertuples()]; ax.axhline(0,linewidth=1); ax.set_xlabel('Task competence: Spearman rho'); ax.set_ylabel('Decision leakage'); ax.set_title('Task competence versus leakage'); fig.tight_layout(); fig.savefig(figs/'08_competence_vs_leakage.png',dpi=180); plt.close(fig)

    summary={'expected_rows':expected,'observed_rows':len(df),'semantic_invalid_rows':int((df.parse_status!='ok').sum()),'total_cost_usd':float(df.cost_usd.sum()),'mixed_effects_status':mixed_status,'model_level_coupling':model_coupling,'surname_pair_coupling':pair_coupling}
    (statsdir/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    lines=['# Phase II results','',f"Primary confirmatory dataset: **{len(df):,} model responses** across {len(model_cfg['models'])} frozen model/provider endpoints.",f"Recorded OpenRouter cost: **${df.cost_usd.sum():.4f}**.",f"Semantically invalid primary rows: **{int((df.parse_status!='ok').sum())}**.",'','## Primary latent association','']
    for r in assoc[assoc.contrast=='elite_minus_common'].sort_values('model_label').itertuples(): lines.append(f"- `{r.model_label}`: elite-common **{r.mean_diff:+.2f}** points, 95% bootstrap CI [{r.ci_low:+.2f}, {r.ci_high:+.2f}], p={r.p:.3g}.")
    lines += ['','## Primary decision leakage','']
    for r in leakage.sort_values('model_label').itertuples(): lines.append(f"- `{r.model_label}`: elite-common **{r.mean_diff:+.3f}** score points, 95% bootstrap CI [{r.ci_low:+.3f}, {r.ci_high:+.3f}], standardized {r.standardized_effect:+.3f}; equivalence within ±0.10 SD: **{'yes' if r.equivalent_within_0_10_sd else 'no'}**.")
    lines += ['','## Association-leakage coupling','',f"Across models: Pearson r={model_coupling['pearson_r']:+.3f} (p={model_coupling['pearson_p']:.3g}); Spearman rho={model_coupling['spearman_rho']:+.3f} (p={model_coupling['spearman_p']:.3g}).",f"Across frozen surname-pair × model cells: Pearson r={pair_coupling['pearson_r']:+.3f} (p={pair_coupling['pearson_p']:.3g}); Spearman rho={pair_coupling['spearman_rho']:+.3f} (p={pair_coupling['spearman_p']:.3g}).",'','## Claim boundary','', 'Phase II distinguishes measured surname-status association from consequential decision leakage. A strong association result is not itself evidence of discriminatory decision behavior. Null or equivalent decision effects apply only to the frozen tasks, models, providers, language, and evaluation conditions in this release.','']
    (out/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__': main()
