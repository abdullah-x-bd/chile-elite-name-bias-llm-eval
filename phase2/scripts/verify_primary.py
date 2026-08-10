from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest


def norm(x): return re.sub(r'[^a-z0-9]+','',str(x or '').lower())


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    manifest=load_manifest(ROOT); expected_ids={r['prompt_id'] for r in manifest}
    failures=[]; all_ids=set(); total=0; total_cost=0.0
    for model in cfg['models']:
        fp=ROOT/'results/raw'/f"{model['label']}.jsonl"
        if not fp.exists(): failures.append(f"missing {fp.name}"); continue
        rows=[json.loads(x) for x in fp.read_text(encoding='utf-8').splitlines() if x.strip()]
        total += len(rows); total_cost += sum(float(r.get('cost_usd') or 0) for r in rows)
        pids={r.get('prompt_id') for r in rows}
        if len(rows)!=len(manifest): failures.append(f"{model['label']} row_count {len(rows)} != {len(manifest)}")
        if pids!=expected_ids: failures.append(f"{model['label']} prompt-id set mismatch")
        rids=[r.get('request_identity') for r in rows]
        if len(rids)!=len(set(rids)): failures.append(f"{model['label']} duplicate request identities")
        overlap=all_ids.intersection(rids)
        if overlap: failures.append(f"cross-model duplicate request identities for {model['label']}")
        all_ids.update(rids)
        for r in rows:
            if r.get('requested_model')!=model['request_id']: failures.append(f"requested model mismatch {model['label']} {r.get('prompt_id')}")
            returned=r.get('returned_model')
            if returned not in (model['request_id'],model['canonical_slug']): failures.append(f"returned model mismatch {model['label']} {r.get('prompt_id')}: {returned}")
            rp=norm(r.get('returned_provider')); wanted=norm(model['provider'])
            aliases={'googleaistudio':['google','googleaistudio'],'alibaba':['alibaba','qwen'],'deepinfra':['deepinfra'],'openai':['openai'],'anthropic':['anthropic'],'deepseek':['deepseek'],'mistral':['mistral']}
            if rp and not any(norm(a) in rp or rp in norm(a) for a in aliases.get(wanted,[wanted])): failures.append(f"returned provider mismatch {model['label']} {r.get('prompt_id')}: {r.get('returned_provider')}")
            if r.get('parse_status')!='ok': failures.append(f"semantic invalid {model['label']} {r.get('prompt_id')}: {r.get('semantic_status')}")
    if total!=study['expected_primary_calls']: failures.append(f"total {total} != {study['expected_primary_calls']}")
    if total_cost>study['budget']['hard_limit_usd']: failures.append(f"primary cost ${total_cost:.4f} exceeded total hard limit")
    report={'status':'PASS' if not failures else 'FAIL','rows':total,'expected_rows':study['expected_primary_calls'],'unique_request_identities':len(all_ids),'total_cost_usd':round(total_cost,6),'failures':failures[:200]}
    out=ROOT/'results'; out.mkdir(parents=True,exist_ok=True); (out/'PRIMARY_VERIFICATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    if failures: raise SystemExit('PRIMARY RELEASE VERIFICATION: FAIL')
    print('PRIMARY RELEASE VERIFICATION: PASS')


if __name__=='__main__': main()
