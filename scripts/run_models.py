"""
Placeholder runner.

This file will hold provider calls after API keys are configured locally.

Expected input
prompts/generated_prompts.jsonl

Expected output
outputs/model_outputs.jsonl

Each output row should include the original prompt fields plus these fields.

model
provider
run_id
response_text
raw_response
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    prompts_path = ROOT / "prompts" / "generated_prompts.jsonl"
    outputs_path = ROOT / "outputs" / "model_outputs.jsonl"
    print(f"Read prompts from {prompts_path}")
    print(f"Write outputs to {outputs_path}")
    print("Provider calls will be added after pilot setup.")


if __name__ == "__main__":
    main()
