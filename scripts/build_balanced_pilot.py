import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"

PAIRWISE_PATH = PROMPTS_DIR / "pairwise_v0_1.jsonl"
SINGLE_PATH = PROMPTS_DIR / "single_profile_v0_1.jsonl"
DIAGNOSTIC_PATH = PROMPTS_DIR / "diagnostic_v0_1.jsonl"
PILOT_PATH = PROMPTS_DIR / "pilot_v0_1.jsonl"


def read_jsonl(path):
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def take_evenly(rows, key, total):
    buckets = defaultdict(list)
    for row in rows:
        buckets[row.get(key, "missing")].append(row)

    selected = []
    bucket_keys = sorted(buckets)
    index = 0
    while len(selected) < total and any(index < len(buckets[k]) for k in bucket_keys):
        for k in bucket_keys:
            if index < len(buckets[k]) and len(selected) < total:
                selected.append(buckets[k][index])
        index += 1
    return selected


def main():
    pairwise = read_jsonl(PAIRWISE_PATH)
    single = read_jsonl(SINGLE_PATH)
    diagnostic = read_jsonl(DIAGNOSTIC_PATH)

    # Pairwise already has elite/common inside each prompt.
    # Select across task families so the pilot does not over-sample early generated tasks.
    pilot_pairwise = take_evenly(pairwise, "task_family", 60)

    # Single profile must include both elite coded and common surnames.
    pilot_single = take_evenly(single, "surname_group", 60)

    # Diagnostic must include both elite coded and common surnames.
    pilot_diag = take_evenly(diagnostic, "surname_group", 20)

    pilot = pilot_pairwise + pilot_single + pilot_diag
    write_jsonl(PILOT_PATH, pilot)

    print(f"balanced pairwise: {len(pilot_pairwise)}")
    print(f"balanced single_profile: {len(pilot_single)}")
    print(f"balanced diagnostic: {len(pilot_diag)}")
    print(f"wrote balanced pilot: {len(pilot)} prompts to {PILOT_PATH}")


if __name__ == "__main__":
    main()
