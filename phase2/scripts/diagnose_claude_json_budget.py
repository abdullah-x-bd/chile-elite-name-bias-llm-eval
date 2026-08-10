from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.openrouter import BASE_URL, post_json, request_identity, require_key, verify_frozen_models

TARGET_ID='53144a4f769105421e338696dcc25fcc4f573d62a5ae8774d6d11fd963584e95'


def metadata(resp, label, cap):
    choice=(resp.get('choices') or [{}])[0]; msg=choice.get('message') or {}; content=msg.get('content')
    if isinstance(content,list): text=''.join(str(x.get('text','')) for x in content if isinstance(x,dict))
    elif isinstance(content,str): text=content
    else: text=''
    try: valid_json=bool(text) and isinstance(json.loads(text),dict)
    except Exception: valid_json=False
    usage=resp.get('usage') or {}; refusal=msg.get('refusal')
    return {'mode':label,'max_tokens':cap,'returned_model':resp.get('model'),'provider':resp.get('provider'),'finish_reason':choice.get('finish_reason'),'native_finish_reason':choice.get('native_finish_reason'),'content_length_chars':len(text),'valid_json':valid_json,'refusal_present':bool(refusal),'refusal_length_chars':len(str(refusal)) if refusal else 0,'completion_tokens':usage.get('completion_tokens'),'reasoning_tokens':(usage.get('completion_tokens_details') or {}).get('reasoning_tokens'),'cost_usd':usage.get('cost')}


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='claude_sonnet5')
    verify_frozen_models({'models':[model]},verify_providers=True)
    target=None
    for prompt in load_manifest(ROOT):
        payload=amended_request_payload(model,prompt,study); payload['max_tokens']=160
        rid=request_identity(study['study_id']+'::amendment6::claude-160',model,prompt,payload)
        if rid==TARGET_ID: target=prompt; break
    if target is None: raise RuntimeError('Could not resolve target request identity')
    print('TARGET_PROMPT_ID',target['prompt_id']); print('TARGET_BANK',target['bank'],'DOMAIN',target['domain'],'CONDITION',target['condition'])
    key=require_key()
    variants=[]
    p=amended_request_payload(model,target,study); p['max_tokens']=160; variants.append(('omit-160',p))
    p=amended_request_payload(model,target,study); p['max_tokens']=160; p['reasoning']={'enabled':False,'exclude':True}; variants.append(('disabled-160',p))
    p=amended_request_payload(model,target,study); p['max_tokens']=160; p['reasoning']={'effort':'none','exclude':True}; variants.append(('none-effort-160',p))
    p=amended_request_payload(model,target,study); p['max_tokens']=384; variants.append(('omit-384',p))
    for label,payload in variants:
        try:
            resp=post_json(BASE_URL+'/chat/completions',payload,key)
            print('DIAGNOSTIC_METADATA',json.dumps(metadata(resp,label,payload['max_tokens']),sort_keys=True))
        except Exception as exc:
            print('DIAGNOSTIC_ERROR',json.dumps({'mode':label,'error_type':type(exc).__name__,'http_code':getattr(exc,'code',None)},sort_keys=True))
    raise SystemExit('OUTCOME-BLIND CLAUDE DIAGNOSTIC 7B COMPLETE; scientific values intentionally not printed')

if __name__=='__main__': main()
