from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest

def main():
    models=json.loads((ROOT/'config/models.json').read_text())['models']
    study=json.loads((ROOT/'config/study.json').read_text())
    prompts=load_manifest(ROOT)
    # Conservative offline estimate: Spanish text ~3.5 chars/token, 45 answer tokens, plus 100 reasoning tokens where required.
    input_tokens=sum(max(1,len(p['prompt_text'])/3.5 + 35) for p in prompts)
    rows=[]; total=0
    for m in models:
        out_tokens=45*len(prompts)
        if m.get('reasoning') in ('minimal','low'): out_tokens += 100*len(prompts)
        cost=input_tokens*m['prompt_price_per_token'] + out_tokens*m['completion_price_per_token']
        rows.append((m['label'],cost)); total+=cost
    print(f"Frozen prompts/model: {len(prompts)}")
    for label,cost in rows: print(f"{label:22s} ${cost:.4f}")
    print(f"Conservative estimated total: ${total:.4f}")
    print(f"Hard limit: ${study['budget']['hard_limit_usd']:.2f}")
    if total > study['budget']['hard_limit_usd']: raise SystemExit('FAIL: estimate exceeds hard limit')
if __name__=='__main__': main()
