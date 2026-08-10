from pathlib import Path
import json, random, sys, time, urllib.error
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest, validate_response
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.openrouter import BASE_URL, extract_content, post_json, request_identity, require_key, verify_frozen_models

TARGET_PROMPT_ID='assoc::common_frequency::flores::school_sector::1'


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='mistral_medium35')
    verify_frozen_models({'models':[model]},verify_providers=True)
    prompt=next(p for p in load_manifest(ROOT) if p['prompt_id']==TARGET_PROMPT_ID)
    payload=amended_request_payload(model,prompt,study)
    rid=request_identity(study['study_id']+'::amendment9::mistral-semantic-retry',model,prompt,payload)
    key=require_key(); last=None
    for attempt in range(6):
        t0=time.time()
        try:
            resp=post_json(BASE_URL+'/chat/completions',payload,key)
            content=extract_content(resp)
            if not isinstance(content,str) or not content:
                last=RuntimeError('empty structured content')
            else:
                try: parsed=json.loads(content)
                except json.JSONDecodeError as exc:
                    last=exc
                else:
                    ok,status=validate_response(prompt,parsed)
                    if ok:
                        usage=resp.get('usage') or {}; cost=float(usage.get('cost') or 0.0)
                        row={'request_identity':rid,'protocol_amendment':9,'prompt_id':prompt['prompt_id'],'requested_model':model['request_id'],'expected_canonical_model':model['canonical_slug'],'returned_model':resp.get('model'),'requested_provider':model['provider'],'returned_provider':resp.get('provider'),'generation_id':resp.get('id'),'timestamp_unix':time.time(),'prompt_sha256':prompt['prompt_sha256'],'schema_name':prompt['schema']['name'],'raw_response':resp,'parsed_response':parsed,'finish_reason':resp.get('choices',[{}])[0].get('finish_reason'),'parse_status':'ok','semantic_status':'ok','usage':usage,'cost_usd':cost,'latency_ms':round((time.time()-t0)*1000,2),'retry_count':attempt}
                        out=ROOT/'results'/'mistral_amendment9.jsonl'; out.parent.mkdir(parents=True,exist_ok=True)
                        out.write_text(json.dumps(row,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
                        print('MISTRAL AMENDMENT 9 COMPLETE prompt=',TARGET_PROMPT_ID,'retry_count=',attempt,'cost_usd=',cost)
                        return
                    last=RuntimeError(f'semantic invalid: {status}')
            if attempt<5: time.sleep(min(10,1+attempt))
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as exc:
            last=exc; code=getattr(exc,'code',None)
            if code not in (None,408,409,425,429,500,502,503,504): raise
            if attempt<5: time.sleep(min(30,2**attempt+random.random()))
    raise RuntimeError(f'Mistral Amendment 9 failed after identical-request retries: {last}')

if __name__=='__main__': main()
