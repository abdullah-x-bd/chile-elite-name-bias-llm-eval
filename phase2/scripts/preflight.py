from pathlib import Path
import json, os, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.openrouter import BASE_URL, get_json, require_key, verify_frozen_models


def main():
    key=require_key()
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    models=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    key_info=get_json(BASE_URL+'/key',key).get('data',{})
    remaining=key_info.get('limit_remaining')
    if remaining is not None and float(remaining) < float(study['budget']['hard_limit_usd']):
        raise RuntimeError(f"API key limit_remaining ${float(remaining):.4f} is below frozen hard limit ${float(study['budget']['hard_limit_usd']):.4f}")
    checked=verify_frozen_models(models,verify_providers=True)
    print('OPENROUTER PREFLIGHT: PASS')
    print('key_limit_remaining:', 'unbounded' if remaining is None else f"${float(remaining):.4f}")
    print('key_usage:', f"${float(key_info.get('usage') or 0):.4f}")
    print('models_verified:',len(checked))
    for item in checked:
        print(item['request_id'],item['canonical_slug'],item['provider'],item['provider_status'])


if __name__=='__main__':
    main()
