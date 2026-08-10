# Protocol Amendment 4, outcome-blind execution-budget repair

Date: 2026-08-10

Status: specified before any Phase II scientific response value was inspected.

The GPT-5.4 Nano Amendment 2 primary job produced valid responses through roughly 850 frozen scientific cells. It then stopped because the execution harness required the model-specific cumulative cost plus a conservative USD 0.01 per-call safety allowance to remain below a USD 0.07 cell cap. At approximately USD 0.0600 cumulative spend, this guard prevented another request even though the underlying OpenRouter calls remained inexpensive and no scientific response failure had occurred.

The partial local JSONL artifact was not uploaded. No GPT-5.4 Nano scientific response value was downloaded or inspected.

## Amendment

The complete GPT-5.4 Nano cell is rerun from the beginning with a model-cell cap of USD 0.10.

No scientific setting changes:

- model `openai/gpt-5.4-nano`;
- canonical model `openai/gpt-5.4-nano-20260317`;
- provider `openai`;
- reasoning omitted;
- seed behavior unchanged;
- 80-token output cap unchanged;
- all 1,032 scientific prompts and hashes unchanged;
- structured schemas and semantic validation unchanged;
- hypotheses, estimands, exclusions, and analysis plan unchanged.

The unrecovered first-attempt Nano expenditure is excluded from the scientific dataset but included in project-level expenditure accounting.

## Outcome blindness

The repair is motivated solely by the predeclared cost guard. No scientific output value from Nano or any other model was inspected to specify this amendment.
