import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PROMPTS_DIR = ROOT / "prompts"


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    names = read_csv(DATA_DIR / "name_sets.csv")
    templates = read_csv(DATA_DIR / "prompt_templates.csv")

    elite_names = [n for n in names if n["group"] == "elite_coded" and n["include_in_pilot"].lower() == "yes"]
    common_names = [n for n in names if n["group"] == "common" and n["include_in_pilot"].lower() == "yes"]

    PROMPTS_DIR.mkdir(exist_ok=True)
    out_path = PROMPTS_DIR / "generated_prompts.jsonl"

    count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for template in templates:
            for elite in elite_names:
                for common in common_names:
                    base_id = f"{template['template_id']}_{elite['name_id']}_{common['name_id']}"
                    variants = [
                        ("A", elite["full_name"], common["full_name"]),
                        ("B", common["full_name"], elite["full_name"]),
                    ]
                    for elite_position, name_a, name_b in variants:
                        count += 1
                        prompt = template["template_text"].format(name_a=name_a, name_b=name_b)
                        row = {
                            "prompt_id": f"P{count:05d}",
                            "base_id": base_id,
                            "template_id": template["template_id"],
                            "task_family": template["task_family"],
                            "scenario": template["scenario"],
                            "elite_position": elite_position,
                            "elite_name_id": elite["name_id"],
                            "common_name_id": common["name_id"],
                            "prompt_text": prompt,
                            "expected_answer": template["correct_answer"],
                        }
                        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {count} prompts to {out_path}")


if __name__ == "__main__":
    main()
