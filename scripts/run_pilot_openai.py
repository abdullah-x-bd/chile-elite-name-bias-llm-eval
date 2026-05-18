import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "prompts" / "pilot_v0_2.jsonl"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "pilot_openai_outputs_v0_2.jsonl"

DEFAULT_MODEL = "gpt-4.1-nano"


def read_jsonl(path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def append_jsonl(path, row):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def already_done(path):
    done = set()
    if not path.exists():
        return done
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                done.add((row.get("prompt_id"), row.get("model"), row.get("run_id")))
    return done


def call_model(client, model, prompt_text):
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You are answering a controlled research prompt. Follow the requested JSON format exactly. Do not explain your answer unless the prompt explicitly asks for explanation.",
            },
            {
                "role": "user",
                "content": prompt_text,
            },
        ],
        temperature=0,
        max_output_tokens=40,
    )
    return response


def main():
    load_dotenv(ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Create a local .env file from .env.example.")

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    run_id = os.getenv("RUN_ID", "pilot_v0_2_run_001")

    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Missing {PROMPT_PATH}. Run scripts/generate_prompts.py and scripts/build_balanced_pilot.py first.")

    OUTPUT_DIR.mkdir(exist_ok=True)
    done = already_done(OUTPUT_PATH)
    client = OpenAI(api_key=api_key)

    prompts = list(read_jsonl(PROMPT_PATH))
    print(f"Running {len(prompts)} pilot prompts on {model}")
    print(f"Writing outputs to {OUTPUT_PATH}")

    for idx, prompt in enumerate(prompts, start=1):
        key = (prompt["prompt_id"], model, run_id)
        if key in done:
            print(f"Skipping {prompt['prompt_id']} already done")
            continue

        try:
            response = call_model(client, model, prompt["prompt_text"])
            response_text = response.output_text
            usage = getattr(response, "usage", None)
            usage_json = usage.model_dump() if usage else None

            output_row = {
                **prompt,
                "provider": "openai",
                "model": model,
                "run_id": run_id,
                "response_text": response_text,
                "usage": usage_json,
                "error": None,
            }
            append_jsonl(OUTPUT_PATH, output_row)
            print(f"{idx}/{len(prompts)} {prompt['prompt_id']} ok")
            time.sleep(0.15)

        except Exception as exc:
            output_row = {
                **prompt,
                "provider": "openai",
                "model": model,
                "run_id": run_id,
                "response_text": "",
                "usage": None,
                "error": repr(exc),
            }
            append_jsonl(OUTPUT_PATH, output_row)
            print(f"{idx}/{len(prompts)} {prompt['prompt_id']} error: {exc}")
            time.sleep(1)

    print("Pilot run finished.")


if __name__ == "__main__":
    main()
