from pathlib import Path
import argparse, json, sys, time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.openrouter import BASE_URL, get_json, require_key


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--label',required=True); args=ap.parse_args()
    data=get_json(BASE_URL+'/key',require_key()).get('data',{})
    safe={
        'label':args.label,
        'timestamp_unix':time.time(),
        'usage_usd':float(data.get('usage') or 0),
        'usage_daily_usd':float(data.get('usage_daily') or 0),
        'usage_weekly_usd':float(data.get('usage_weekly') or 0),
        'usage_monthly_usd':float(data.get('usage_monthly') or 0),
        'limit_remaining_usd':None if data.get('limit_remaining') is None else float(data['limit_remaining']),
    }
    out=ROOT/'results'; out.mkdir(parents=True,exist_ok=True)
    (out/f"openrouter_usage_{args.label}.json").write_text(json.dumps(safe,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(safe,indent=2,sort_keys=True))


if __name__=='__main__': main()
