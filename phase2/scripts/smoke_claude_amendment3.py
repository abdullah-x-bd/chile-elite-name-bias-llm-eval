from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import DECISION_SCHEMA, sha256_text
from chile_phase2.execution_amendment3 import run_exact_amendment3
from chile_phase2.openrouter import verify_frozen_models


def main():
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    cfg=json.loads((ROOT/'config/models.json').read_text(encoding='utf-8'))
    model=next(m for m in cfg['models'] if m['label']=='claude_sonnet5')
    verify_frozen_models({'models':[model]},verify_providers=True)
    text='Prueba técnica no científica. Devuelve exactamente score=50, recommendation="advance" y confidence=50 en el esquema JSON solicitado.'
    prompt={'prompt_id':'technical-smoke::claude_amendment3','bank':'decision_main','domain':'technical_smoke','instrument':'technical_smoke','base_profile_id':None,'condition':'technical_smoke','surname':None,'surname_group':'none','given_name':None,'visibility':'none','decision_mode':'structured','schema':DECISION_SCHEMA,'prompt_text':text,'prompt_sha256':sha256_text(text)}
    result=run_exact_amendment3(model,prompt,study,0.0,max_retries=3)
    if result['parsed_response']!={'score':50,'recommendation':'advance','confidence':50}:
        raise RuntimeError(result['parsed_response'])
    print('CLAUDE AMENDMENT 3 SMOKE: PASS','cost=',result.get('cost_usd'))

if __name__=='__main__': main()
