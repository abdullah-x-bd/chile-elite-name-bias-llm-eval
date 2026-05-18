import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"

PAIRWISE_EQUAL_PATH = PROMPTS_DIR / "pairwise_equal_v0_2.jsonl"
PAIRWISE_FORCED_PATH = PROMPTS_DIR / "pairwise_forced_v0_2.jsonl"
SINGLE_PATH = PROMPTS_DIR / "single_profile_v0_2.jsonl"
DIAGNOSTIC_PATH = PROMPTS_DIR / "diagnostic_v0_2.jsonl"
PILOT_PATH = PROMPTS_DIR / "pilot_v0_2.jsonl"


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
    pairwise_equal = read_jsonl(PAIRWISE_EQUAL_PATH)
    pairwise_forced = read_jsonl(PAIRWISE_FORCED_PATH)
    single = read_jsonl(SINGLE_PATH)
    diagnostic = read_jsonl(DIAGNOSTIC_PATH)

    pilot_equal = take_evenly(pairwise_equal, "task_family", 40)
    pilot_forced = take_evenly(pairwise_forced, "task_family", 40)
    pilot_single = take_evenly(single, "surname_group", 40)
    pilot_diag = take_evenly(diagnostic, "surname_group", 20)

    pilot = pilot_equal + pilot_forced + pilot_single + pilot_diag
    write_jsonl(PILOT_PATH, pilot)

    print(f"balanced pairwise_equal: {len(pilot_equal)}")
    print(f"balanced pairwise_forced: {len(pilot_forced)}")
    print(f"balanced single_profile: {len(pilot_single)}")
    print(f"balanced diagnostic: {len(pilot_diag)}")
    print(f"wrote balanced pilot: {len(pilot)} prompts to {PILOT_PATH}")


if __name__ == "__main__":
    main()
