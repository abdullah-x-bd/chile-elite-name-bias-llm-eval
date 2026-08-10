from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.openrouter import BASE_URL, get_json, require_key

ALLOWANCE=0.80
CEILING=6.75


def main():
    data=get_json(BASE_URL+'/key',require_key()).get('data',{})
    usage=float(data.get('usage') or 0)
    print(f'current_key_usage_usd={usage:.6f}')
    print(f'robustness_allowance_usd={ALLOWANCE:.2f}')
    print(f'project_ceiling_usd={CEILING:.2f}')
    if usage+ALLOWANCE>CEILING:
        raise SystemExit(f'ROBUSTNESS BUDGET GATE: STOP, ${usage:.4f}+${ALLOWANCE:.2f}>${CEILING:.2f}')
    print('ROBUSTNESS BUDGET GATE: PASS')

if __name__=='__main__': main()
