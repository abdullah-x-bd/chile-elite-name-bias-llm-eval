from pathlib import Path
import argparse, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from chile_phase2.core import generate_profiles, generate_manifest, compact_manifest, write_jsonl, write_manifest_parts, load_jsonl, validate_manifest

def file_hash(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--verify',action='store_true'); args=ap.parse_args()
    study=json.loads((ROOT/'config/study.json').read_text(encoding='utf-8'))
    profiles=generate_profiles(study['seed'],study['profiles_per_domain'])
    write_jsonl(ROOT/'data/frozen/base_profiles_v1.jsonl.gz.b64',profiles)
    manifest=generate_manifest(ROOT,profiles)
    write_manifest_parts(ROOT,compact_manifest(manifest))
    validate_manifest(manifest,profiles)
    if args.verify:
        assert len(profiles)==192 and len(manifest)==study['expected_prompts_per_model']
    print(json.dumps({'profiles':len(profiles),'prompts_per_model':len(manifest),'planned_calls':len(manifest)*study['expected_models']},indent=2))
if __name__=='__main__': main()
