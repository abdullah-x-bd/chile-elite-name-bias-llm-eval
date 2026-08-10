from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.openrouter import verify_frozen_models

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--verify-frozen',action='store_true'); args=ap.parse_args()
    cfg=json.loads((ROOT/'config/models.json').read_text())
    checked=verify_frozen_models(cfg)
    print(json.dumps({'status':'PASS','models':checked},indent=2))
if __name__=='__main__': main()
