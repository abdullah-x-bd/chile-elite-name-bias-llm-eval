from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.robustness import BANK_TARGETS, deterministic_subset, english_prompt


def digest(rows):
    payload=''.join(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n' for r in rows)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def main():
    subset=deterministic_subset(ROOT)
    english=[english_prompt(ROOT,r) for r in subset]
    compact=[{'prompt_id':r['prompt_id'],'bank':r['bank'],'prompt_sha256':r['prompt_sha256']} for r in subset]
    compact_en=[{'prompt_id':r['prompt_id'],'bank':r['bank'],'prompt_sha256':r['prompt_sha256']} for r in english]
    obj={
        'version':'robustness-v1',
        'outcome_blind':True,
        'spanish_subset_count':len(subset),
        'bank_targets':BANK_TARGETS,
        'spanish_subset_digest_sha256':digest(compact),
        'english_subset_digest_sha256':digest(compact_en),
        'planned_calls':{'repeated_stability':832,'english_context_shift':416,'provider_sensitivity':52,'total':1300},
        'spanish_cells':compact,
        'english_cells':compact_en,
    }
    out=ROOT/'freeze/robustness_manifest.json'
    out.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in obj.items() if not k.endswith('_cells')},indent=2,sort_keys=True))


if __name__=='__main__': main()
