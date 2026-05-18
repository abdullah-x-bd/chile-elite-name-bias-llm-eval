import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"

INPUT_FILES = [
    PROMPTS_DIR / "pairwise_equal_v0_2.jsonl",
    PROMPTS_DIR / "pairwise_forced_v0_2.jsonl",
    PROMPTS_DIR / "single_profile_v0_2.jsonl",
    PROMPTS_DIR / "diagnostic_v0_2.jsonl",
]
OUTPUT_PATH = PROMPTS_DIR / "full_v0_2.jsonl"


def read_jsonl(path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def main():
    rows = []
    counts = {}
    for path in INPUT_FILES:
        file_rows = list(read_jsonl(path))
        counts[path.name] = len(file_rows)
        rows.extend(file_rows)

    write_jsonl(OUTPUT_PATH, rows)

    for name, count in counts.items():
        print(f"{name}: {count}")
    print(f"full_v0_2.jsonl: {len(rows)} prompts")


if __name__ == "__main__":
    main()
