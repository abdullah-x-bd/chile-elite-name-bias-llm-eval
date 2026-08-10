from pathlib import Path
import copy, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import DECISION_SCHEMA, sha256_text, validate_response
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.openrouter import BASE_URL, extract_content, post_json, require_key, verify_frozen_models


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='deepseek_v32')
    verify_frozen_models({'models':[model]},verify_providers=True)
    text='Prueba técnica no científica. Devuelve exactamente score=50, recommendation="advance" y confidence=50 en el esquema JSON solicitado.'
    prompt={'prompt_id':'technical-diagnostic::deepseek_v32','bank':'decision_main','domain':'technical_diagnostic','instrument':'technical_diagnostic','base_profile_id':None,'condition':'technical_diagnostic','surname':None,'surname_group':'none','given_name':None,'visibility':'none','decision_mode':'structured','schema':DECISION_SCHEMA,'prompt_text':text,'prompt_sha256':sha256_text(text)}
    base=amended_request_payload(model,prompt,study)
    variants=[]
    a=copy.deepcopy(base); a['reasoning']={'enabled':False,'exclude':True}; variants.append(('reasoning_disabled_80',a))
    b=copy.deepcopy(base); b.pop('reasoning',None); variants.append(('reasoning_omitted_80',b))
    c=copy.deepcopy(base); c['reasoning']={'effort':'low','exclude':True}; c['max_tokens']=256; variants.append(('reasoning_low_256',c))
    successes=[]; key=require_key()
    for name,payload in variants:
        try:
            resp=post_json(BASE_URL+'/chat/completions',payload,key)
            msg=(resp.get('choices') or [{}])[0].get('message') or {}
            content=extract_content(resp)
            usage=resp.get('usage') or {}
            print('VARIANT',name,'returned_model=',resp.get('model'),'provider=',resp.get('provider'),'finish_reason=',(resp.get('choices') or [{}])[0].get('finish_reason'),'content_is_none=',content is None,'content_len=',len(content) if isinstance(content,str) else None,'reasoning_len=',len(str(msg.get('reasoning') or msg.get('reasoning_content') or '')),'usage=',json.dumps(usage,sort_keys=True))
            if isinstance(content,str) and content:
                parsed=json.loads(content); ok,status=validate_response(prompt,parsed)
                print('PARSED',name,json.dumps(parsed,sort_keys=True),'semantic=',ok,status)
                if ok and parsed=={'score':50,'recommendation':'advance','confidence':50}: successes.append(name)
        except Exception as exc:
            print('VARIANT_ERROR',name,repr(exc))
    print('SUCCESSFUL_VARIANTS',json.dumps(successes))
    raise SystemExit('DIAGNOSTIC COMPLETE: workflow intentionally stopped before scientific execution')


if __name__=='__main__': main()
