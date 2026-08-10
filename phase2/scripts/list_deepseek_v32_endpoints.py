import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.openrouter import BASE_URL, get_json, public_models


def main():
    slug='deepseek/deepseek-v3.2'
    models=public_models()
    if slug not in models: raise RuntimeError(f'{slug} not in live model catalogue')
    m=models[slug]
    print('request_id',slug)
    print('canonical_slug',m.get('canonical_slug'))
    print('pricing',json.dumps(m.get('pricing',{}),sort_keys=True))
    print('supported_parameters',json.dumps(m.get('supported_parameters',[])))
    details=(m.get('links') or {}).get('details')
    data=get_json('https://openrouter.ai'+details).get('data',{})
    for ep in data.get('endpoints',[]):
        print('ENDPOINT',json.dumps({'tag':ep.get('tag'),'provider_name':ep.get('provider_name'),'status':ep.get('status'),'supports_tool_parameters':ep.get('supports_tool_parameters'),'pricing':ep.get('pricing')},sort_keys=True))


if __name__=='__main__': main()
