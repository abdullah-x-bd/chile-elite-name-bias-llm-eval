from pathlib import Path
import copy, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.execution_amendment1 import amended_request_payload
from chile_phase2.openrouter import BASE_URL, post_json, request_identity, require_key, verify_frozen_models

TARGET_ID='1246482029fa7def1fc213174504b8812f64ee659b2ad7f42b03a2c1b048ac15'


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='claude_sonnet5')
    verify_frozen_models({'models':[model]},verify_providers=True)
    target=None
    for prompt in load_manifest(ROOT):
        payload=amended_request_payload(model,prompt,study)
        rid=request_identity(study['study_id']+'::amendment3::claude-repair',model,prompt,payload)
        if rid==TARGET_ID:
            target=prompt; break
    if target is None: raise RuntimeError('Could not resolve failing Claude request identity')
    print('TARGET_PROMPT_ID',target['prompt_id'])
    print('TARGET_BANK',target['bank'],'DOMAIN',target['domain'],'CONDITION',target['condition'])
    key=require_key()
    for cap in (80,160):
        payload=amended_request_payload(model,target,study); payload['max_tokens']=cap
        resp=post_json(BASE_URL+'/chat/completions',payload,key)
        choice=(resp.get('choices') or [{}])[0]; msg=choice.get('message') or {}; content=msg.get('content')
        if isinstance(content,list): content_len=sum(len(str(x.get('text',''))) for x in content if isinstance(x,dict))
        elif isinstance(content,str): content_len=len(content)
        else: content_len=0
        refusal=msg.get('refusal')
        usage=resp.get('usage') or {}
        safe={
            'max_tokens':cap,
            'returned_model':resp.get('model'),
            'provider':resp.get('provider'),
            'finish_reason':choice.get('finish_reason'),
            'native_finish_reason':choice.get('native_finish_reason'),
            'message_keys':sorted(msg.keys()),
            'content_present':content_len>0,
            'content_length_chars':content_len,
            'refusal_present':bool(refusal),
            'refusal_length_chars':len(str(refusal)) if refusal else 0,
            'completion_tokens':usage.get('completion_tokens'),
            'reasoning_tokens':(usage.get('completion_tokens_details') or {}).get('reasoning_tokens'),
            'cost_usd':usage.get('cost'),
        }
        print('DIAGNOSTIC_METADATA',json.dumps(safe,sort_keys=True))
    raise SystemExit('OUTCOME-BLIND CLAUDE DIAGNOSTIC COMPLETE; scientific content intentionally not printed')

if __name__=='__main__': main()
