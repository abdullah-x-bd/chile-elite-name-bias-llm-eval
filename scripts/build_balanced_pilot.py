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


def take_matched_pairwise(rows, total):
    if total % 2 != 0:
        raise ValueError("Pairwise pilot total must be even so A/B counterbalanced rows stay matched.")

    groups = defaultdict(list)
    for row in rows:
        key = (row["pair_id"], row["template_id"])
        groups[key].append(row)

    matched_groups = []
    for key, group_rows in groups.items():
        positions = {r.get("elite_position") for r in group_rows}
        if positions == {"A", "B"} and len(group_rows) == 2:
            matched_groups.append(group_rows)

    by_task = defaultdict(list)
    for group_rows in matched_groups:
        task = group_rows[0].get("task_family", "missing")
        ordered = sorted(group_rows, key=lambda r: r.get("elite_position", ""))
        by_task[task].append(ordered)

    selected = []
    task_keys = sorted(by_task)
    pair_index = 0
    target_pairs = total // 2

    while len(selected) < target_pairs and any(pair_index < len(by_task[k]) for k in task_keys):
        for task in task_keys:
            if pair_index < len(by_task[task]) and len(selected) < target_pairs:
                selected.append(by_task[task][pair_index])
        pair_index += 1

    flat = [row for pair_rows in selected for row in pair_rows]
    if len(flat) != total:
        raise RuntimeError(f"Could only build {len(flat)} matched pairwise rows, wanted {total}.")
    return flat


def main():
    pairwise_equal = read_jsonl(PAIRWISE_EQUAL_PATH)
    pairwise_forced = read_jsonl(PAIRWISE_FORCED_PATH)
    single = read_jsonl(SINGLE_PATH)
    diagnostic = read_jsonl(DIAGNOSTIC_PATH)

    # Pairwise prompts must preserve matched A/B counterbalanced pairs.
    # This prevents option-position bias from being misread as surname bias.
    pilot_equal = take_matched_pairwise(pairwise_equal, 40)
    pilot_forced = take_matched_pairwise(pairwise_forced, 40)

    # Single profile and diagnostic prompts should stay balanced by surname group.
    pilot_single = take_evenly(single, "surname_group", 40)
    pilot_diag = take_evenly(diagnostic, "surname_group", 20)

    pilot = pilot_equal + pilot_forced + pilot_single + pilot_diag
    write_jsonl(PILOT_PATH, pilot)

    print(f"matched pairwise_equal: {len(pilot_equal)} rows, {len(pilot_equal) // 2} matched pairs")
    print(f"matched pairwise_forced: {len(pilot_forced)} rows, {len(pilot_forced) // 2} matched pairs")
    print(f"balanced single_profile: {len(pilot_single)}")
    print(f"balanced diagnostic: {len(pilot_diag)}")
    print(f"wrote balanced pilot: {len(pilot)} prompts to {PILOT_PATH}")


if __name__ == "__main__":
    main()
