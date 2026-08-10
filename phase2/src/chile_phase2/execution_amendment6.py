from __future__ import annotations
import json, random, time, urllib.error
from chile_phase2.core import validate_response
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.openrouter import BASE_URL, extract_content, post_json, request_identity, require_key

CLAUDE_MAX_TOKENS=160


def run_claude_amendment6(model: dict, prompt: dict, study: dict, cumulative_cost: float, max_retries: int=5) -> dict:
    if model.get('label')!='claude_sonnet5' or model.get('provider')!='anthropic' or model.get('reasoning')!='omit':
        raise RuntimeError('Amendment 6 is defined only for Claude Sonnet 5 / Anthropic / reasoning omitted')
    key=require_key(); payload=amended_request_payload(model,prompt,study); payload['max_tokens']=CLAUDE_MAX_TOKENS
    identity=request_identity(study['study_id']+'::amendment6::claude-160',model,prompt,payload)
    last=None
    for attempt in range(max_retries+1):
        t0=time.time()
        try:
            resp=post_json(BASE_URL+'/chat/completions',payload,key)
            content=extract_content(resp)
            if not isinstance(content,str) or not content:
                last=RuntimeError(f'Provider returned no final structured content for {identity}')
                if attempt>=max_retries: raise last
                time.sleep(min(10,1+attempt)); continue
            try:
                parsed=json.loads(content)
            except json.JSONDecodeError as exc:
                last=exc
                if attempt>=max_retries: raise RuntimeError(f'Claude structured response remained invalid JSON for {identity}') from exc
                time.sleep(min(10,1+attempt)); continue
            semantic_ok,semantic_status=validate_response(prompt,parsed)
            usage=resp.get('usage') or {}; cost=float(usage.get('cost') or 0.0)
            return {
                'request_identity':identity,'protocol_amendment':6,'prompt_id':prompt['prompt_id'],
                'requested_model':model['request_id'],'expected_canonical_model':model['canonical_slug'],
                'returned_model':resp.get('model'),'requested_provider':model['provider'],'returned_provider':resp.get('provider'),
                'generation_id':resp.get('id'),'timestamp_unix':time.time(),'prompt_sha256':prompt['prompt_sha256'],
                'schema_name':prompt['schema']['name'],'raw_response':resp,'parsed_response':parsed,
                'finish_reason':resp.get('choices',[{}])[0].get('finish_reason'),
                'parse_status':'ok' if semantic_ok else 'semantic_invalid','semantic_status':semantic_status,
                'usage':usage,'cost_usd':cost,'latency_ms':round((time.time()-t0)*1000,2),'retry_count':attempt,
                'max_tokens_effective':CLAUDE_MAX_TOKENS,
            }
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as exc:
            last=exc; code=getattr(exc,'code',None)
            if code not in (None,408,409,425,429,500,502,503,504): raise
            if attempt>=max_retries: break
            time.sleep(min(30,2**attempt+random.random()))
    raise RuntimeError(f'Claude Amendment 6 request failed after retries: {last}')
