from pathlib import Path
import argparse, json, sys, urllib.error
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import DECISION_SCHEMA, sha256_text
from chile_phase2.openrouter import verify_frozen_models
from chile_phase2.execution_amendment2 import run_exact_amendment2


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--label',required=True); args=ap.parse_args()
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']==args.label)
    verify_frozen_models({'models':[model]},verify_providers=True)
    text='Prueba técnica no científica. Devuelve exactamente score=50, recommendation="advance" y confidence=50 en el esquema JSON solicitado.'
    prompt={'prompt_id':f"technical-smoke::{args.label}",'bank':'decision_main','domain':'technical_smoke','instrument':'technical_smoke','base_profile_id':None,'condition':'technical_smoke','surname':None,'surname_group':'none','given_name':None,'visibility':'none','decision_mode':'structured','schema':DECISION_SCHEMA,'prompt_text':text,'prompt_sha256':sha256_text(text)}
    try:
        result=run_exact_amendment2(model,prompt,study,0.0,max_retries=3)
    except urllib.error.HTTPError as exc:
        body=exc.read().decode('utf-8','replace')
        raise RuntimeError(f"OpenRouter smoke HTTP {exc.code} for {args.label}: {body[:3000]}") from exc
    parsed=result['parsed_response']
    if parsed != {'score':50,'recommendation':'advance','confidence':50}:
        raise RuntimeError(f"Smoke output mismatch for {args.label}: {parsed}")
    print('SMOKE PASS',args.label,'returned_model=',result.get('returned_model'),'provider=',result.get('returned_provider'),'cost=',result.get('cost_usd'))


if __name__=='__main__': main()
