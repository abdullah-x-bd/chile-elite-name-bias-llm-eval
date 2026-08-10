from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest, load_jsonl
from chile_phase2.openrouter import request_identity, request_payload


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    manifest=load_manifest(ROOT); profiles={p['profile_id']:p for p in load_jsonl(ROOT/'data/frozen/base_profiles_v1.jsonl.gz.b64')}
    outdir=ROOT/'results/raw'; outdir.mkdir(parents=True,exist_ok=True)
    for mi,model in enumerate(cfg['models']):
        rows=[]
        for prompt in manifest:
            if prompt['bank']=='association':
                high={'elite_coded':70,'common_frequency':55,'rare_frequency':54}[prompt['surname_group']] + (mi%3-1)
                if prompt['domain']=='university_prestige': parsed={'high_prestige':high,'middle_tier':20,'broad_access':80-high}
                else: parsed={'private_paid':high,'subsidized_private':20,'public':80-high}
                if prompt['instrument'].endswith('_abstention'):
                    parsed['can_infer']=prompt['surname_group']=='elite_coded'
                    if not parsed['can_infer']:
                        for k in [x for x in parsed if x!='can_infer']: parsed[k]=0
            else:
                base=profiles[prompt['base_profile_id']]['normative_score']
                shift=0
                if prompt['condition'] in ('elite','elite_metadata'): shift=1.0 + .1*mi
                if prompt['condition']=='rare': shift=.2
                if prompt['bank']=='decision_holistic' and prompt['condition']=='elite': shift+=1
                score=int(max(0,min(100,round(base+shift))))
                parsed={'score':score,'recommendation':'advance' if score>=60 else 'do_not_advance','confidence':75}
            payload=request_payload(model,prompt,study); rid=request_identity(study['study_id'],model,prompt,payload)
            rows.append({'request_identity':rid,'prompt_id':prompt['prompt_id'],'requested_model':model['request_id'],'expected_canonical_model':model['canonical_slug'],'returned_model':model['canonical_slug'],'requested_provider':model['provider'],'returned_provider':model['provider'],'generation_id':'synthetic','timestamp_unix':0,'prompt_sha256':prompt['prompt_sha256'],'schema_name':prompt['schema']['name'],'raw_response':{},'parsed_response':parsed,'finish_reason':'stop','parse_status':'ok','semantic_status':'ok','usage':{},'cost_usd':0.0,'latency_ms':1.0,'retry_count':0})
        (outdir/f"{model['label']}.jsonl").write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf-8')
    print('SYNTHETIC FIXTURE WRITTEN',len(cfg['models'])*len(manifest),'rows')


if __name__=='__main__': main()
