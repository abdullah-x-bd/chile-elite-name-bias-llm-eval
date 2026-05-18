import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


def pct(n, d):
    if d == 0:
        return 0.0
    return round(100 * n / d, 2)


def summarize(rows, group_key):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row.get(group_key, "all")].append(row)

    summaries = []
    for key, items in grouped.items():
        valid = [r for r in items if r["is_valid"] == "True"]
        unequal = [r for r in valid if r["is_unequal"] == "True"]
        prefs = Counter(r["preference"] for r in valid)
        summaries.append({
            group_key: key,
            "n_total": len(items),
            "n_valid": len(valid),
            "equal_rate": pct(prefs["equal"], len(valid)),
            "elite_preference_rate": pct(prefs["elite_coded"], len(valid)),
            "common_preference_rate": pct(prefs["common"], len(valid)),
            "elite_share_of_unequal": pct(sum(1 for r in unequal if r["preference"] == "elite_coded"), len(unequal)),
            "high_confidence_unequal_rate": pct(sum(1 for r in valid if r["is_high_confidence_unequal"] == "True"), len(valid)),
            "status_coded_reason_rate": pct(sum(1 for r in valid if r["status_coded_reason"] == "True"), len(valid)),
            "fairness_correction_rate": pct(sum(1 for r in valid if r["fairness_correction"] == "True"), len(valid)),
        })
    return summaries


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    input_path = RESULTS_DIR / "scored_outputs.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Expected {input_path}. Run score_outputs.py first.")

    with input_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    write_csv(RESULTS_DIR / "model_summary.csv", summarize(rows, "model"))
    write_csv(RESULTS_DIR / "task_family_summary.csv", summarize(rows, "task_family"))

    print("Wrote summary files to results/")


if __name__ == "__main__":
    main()
