from pathlib import Path
import json, os, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import load_manifest
from chile_phase2.openrouter import require_key, verify_frozen_models, request_payload, request_identity, run_exact

def main():
    require_key()
    study=json.loads((ROOT/'config/study.json').read_text())
    if study.get('scientific_calls_started') is not False: raise RuntimeError('Unexpected study state')
    models_cfg=json.loads((ROOT/'config/models.json').read_text())
    verify_frozen_models(models_cfg)
    manifest=load_manifest(ROOT)
    results_dir=ROOT/'results/raw'; results_dir.mkdir(parents=True,exist_ok=True)
    cumulative=0.0
    # Resume cost from committed/local successful outputs.
    for fp in results_dir.glob('*.jsonl'):
        for line in fp.read_text(encoding='utf-8').splitlines():
            if line.strip(): cumulative += float(json.loads(line).get('cost_usd') or 0)
    for model in models_cfg['models']:
        out=results_dir/f"{model['label']}.jsonl"
        done=set()
        if out.exists():
            for line in out.read_text(encoding='utf-8').splitlines():
                if line.strip(): done.add(json.loads(line)['request_identity'])
        with out.open('a',encoding='utf-8') as f:
            for prompt in manifest:
                payload=request_payload(model,prompt,study); rid=request_identity(study['study_id'],model,prompt,payload)
                if rid in done: continue
                result=run_exact(model,prompt,study,cumulative)
                cumulative += result['cost_usd']
                f.write(json.dumps(result,ensure_ascii=False,sort_keys=True)+"\n"); f.flush()
                print(model['label'],prompt['prompt_id'],f"${cumulative:.4f}")
    print(f"COMPLETE. actual recorded cost ${cumulative:.4f}")
if __name__=='__main__': main()
