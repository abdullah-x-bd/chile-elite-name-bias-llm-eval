from __future__ import annotations
import hashlib, json, os, random, time, urllib.error, urllib.request
from pathlib import Path
from chile_phase2.core import validate_response

BASE_URL="https://openrouter.ai/api/v1"

def require_key() -> str:
    key=os.environ.get("OPENROUTER_API_KEY","").strip()
    if not key: raise RuntimeError("OPENROUTER_API_KEY is not set")
    return key

def get_json(url: str, key: str|None=None) -> dict:
    headers={"User-Agent":"chile-phase2-research/0.1"}
    if key: headers["Authorization"]=f"Bearer {key}"
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=60) as resp: return json.loads(resp.read().decode("utf-8"))

def post_json(url: str, payload: dict, key: str) -> dict:
    data=json.dumps(payload,ensure_ascii=False).encode('utf-8')
    req=urllib.request.Request(url,data=data,method='POST',headers={"Authorization":f"Bearer {key}","Content-Type":"application/json","User-Agent":"chile-phase2-research/0.1"})
    with urllib.request.urlopen(req,timeout=180) as resp: return json.loads(resp.read().decode('utf-8'))

def public_models() -> dict[str,dict]:
    return {m['id']:m for m in get_json(BASE_URL+'/models')['data']}

def verify_frozen_models(models_cfg: dict, verify_providers: bool=True) -> list[dict]:
    live=public_models(); checked=[]
    for m in models_cfg['models']:
        if m['request_id'] not in live: raise RuntimeError(f"Frozen model unavailable: {m['request_id']}")
        got=live[m['request_id']]
        if got.get('canonical_slug') != m['canonical_slug']:
            raise RuntimeError(f"Canonical slug changed for {m['request_id']}: {got.get('canonical_slug')} != {m['canonical_slug']}")
        if 'response_format' not in got.get('supported_parameters',[]) and 'structured_outputs' not in got.get('supported_parameters',[]):
            raise RuntimeError(f"Frozen model lacks structured output support: {m['request_id']}")
        provider_status='not_checked'
        if verify_providers:
            details=(got.get('links') or {}).get('details')
            if not details: raise RuntimeError(f"No endpoint-details link for {m['request_id']}")
            endpoint_data=get_json('https://openrouter.ai'+details).get('data',{})
            endpoints=endpoint_data.get('endpoints',[])
            wanted=m['provider'].lower()
            matched=[]
            for ep in endpoints:
                tag=str(ep.get('tag') or '').lower()
                pname=str(ep.get('provider_name') or '').lower().replace(' ','-')
                if tag.startswith(wanted+'/') or tag==wanted or wanted in pname:
                    matched.append(ep)
            if not matched:
                # Known native-provider names are sometimes display-normalized differently.
                aliases={'google-ai-studio':['google','google-ai-studio'],'alibaba':['alibaba'],'deepinfra':['deepinfra'],'openai':['openai'],'anthropic':['anthropic'],'deepseek':['deepseek'],'mistral':['mistral']}
                for ep in endpoints:
                    hay=(str(ep.get('tag') or '')+' '+str(ep.get('provider_name') or '')).lower()
                    if any(a in hay for a in aliases.get(wanted,[wanted])): matched.append(ep)
            if not matched: raise RuntimeError(f"Pinned provider {m['provider']} unavailable for {m['request_id']}")
            provider_status='available'
        checked.append({'request_id':m['request_id'],'canonical_slug':got.get('canonical_slug'),'provider':m['provider'],'provider_status':provider_status,'supported_parameters':got.get('supported_parameters',[]),'pricing':got.get('pricing',{})})
    return checked

def response_format(schema: dict) -> dict:
    return {"type":"json_schema","json_schema":schema}

def request_payload(model: dict, prompt: dict, study: dict) -> dict:
    payload={
      "model":model['request_id'],
      "messages":[
        {"role":"system","content":"Participas en un estudio controlado. Sigue exactamente el esquema JSON solicitado. No entregues explicación ni razonamiento."},
        {"role":"user","content":prompt['prompt_text']}],
      "max_tokens":study['inference']['max_tokens'],
      "stream":False,
      "response_format":response_format(prompt['schema']),
      "provider":{"order":[model['provider']],"allow_fallbacks":False,"require_parameters":True},
      "usage":{"include":True}
    }
    if model.get('supports_temperature'): payload['temperature']=0
    if model.get('supports_seed'): payload['seed']=study['seed']
    reasoning=model.get('reasoning','none')
    if reasoning == 'minimal': payload['reasoning']={"effort":"minimal","exclude":True}
    elif reasoning == 'low': payload['reasoning']={"effort":"low","exclude":True}
    elif reasoning == 'disabled': payload['reasoning']={"enabled":False,"exclude":True}
    elif reasoning == 'none_effort': payload['reasoning']={"effort":"none","exclude":True}
    # 'omit' intentionally sends no reasoning parameter.
    return payload

def request_identity(study_id: str, model: dict, prompt: dict, payload: dict) -> str:
    stable={"study_id":study_id,"model":model['request_id'],"canonical":model['canonical_slug'],"provider":model['provider'],"prompt_id":prompt['prompt_id'],"prompt_sha256":prompt['prompt_sha256'],"parameters":{k:v for k,v in payload.items() if k not in ['messages']}}
    return hashlib.sha256(json.dumps(stable,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def extract_content(resp: dict):
    msg=resp['choices'][0]['message']; content=msg.get('content','')
    if isinstance(content,list):
        content=''.join(x.get('text','') for x in content if isinstance(x,dict))
    return content

def run_exact(model: dict, prompt: dict, study: dict, cumulative_cost: float, max_retries: int=5) -> dict:
    key=require_key(); payload=request_payload(model,prompt,study)
    identity=request_identity(study['study_id'],model,prompt,payload)
    allowance=study['budget']['per_call_safety_allowance_usd']
    if cumulative_cost + allowance > study['budget']['hard_limit_usd']:
        raise RuntimeError("Budget guard stopped execution before request")
    last=None
    for attempt in range(max_retries+1):
        t0=time.time()
        try:
            resp=post_json(BASE_URL+'/chat/completions',payload,key)
            content=extract_content(resp); parsed=json.loads(content)
            semantic_ok, semantic_status=validate_response(prompt,parsed)
            usage=resp.get('usage') or {}
            cost=float(usage.get('cost') or 0.0)
            return {"request_identity":identity,"prompt_id":prompt['prompt_id'],"requested_model":model['request_id'],"expected_canonical_model":model['canonical_slug'],"returned_model":resp.get('model'),"requested_provider":model['provider'],"returned_provider":resp.get('provider'),"generation_id":resp.get('id'),"timestamp_unix":time.time(),"prompt_sha256":prompt['prompt_sha256'],"schema_name":prompt['schema']['name'],"raw_response":resp,"parsed_response":parsed,"finish_reason":resp.get('choices',[{}])[0].get('finish_reason'),"parse_status":"ok" if semantic_ok else "semantic_invalid","semantic_status":semantic_status,"usage":usage,"cost_usd":cost,"latency_ms":round((time.time()-t0)*1000,2),"retry_count":attempt}
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last=exc
            code=getattr(exc,'code',None)
            if code not in (None,408,409,425,429,500,502,503,504): raise
            if attempt>=max_retries: break
            time.sleep(min(30,2**attempt + random.random()))
        except json.JSONDecodeError:
            raise RuntimeError(f"Schema response was not valid JSON for {identity}")
    raise RuntimeError(f"Exact request failed after retries: {last}")

def cli_run():
    raise SystemExit("Use scripts/run_confirmatory.py after the scientific freeze is merged and verified.")
