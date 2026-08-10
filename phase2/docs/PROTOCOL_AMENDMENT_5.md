# Protocol Amendment 5, outcome-blind structured-output retry repair

Date: 2026-08-10

Status: specified before any Phase II scientific response value was inspected.

The DeepSeek V3.2 / DeepInfra Amendment 2 primary cell completed 500 frozen scientific cells at approximately USD 0.0230 cumulative cost. A later response contained truncated JSON and the Amendment 2 adapter aborted immediately on `JSONDecodeError`. The partial local JSONL artifact was not uploaded, and no DeepSeek scientific response value was downloaded or inspected.

## Amendment

The complete DeepSeek V3.2 cell is rerun from the beginning. If a provider response is non-empty but not syntactically valid JSON, the runner retries the identical frozen request up to the same bounded retry limit already used for transient transport failures.

No scientific setting changes:

- model `deepseek/deepseek-v3.2`;
- canonical model `deepseek/deepseek-v3.2-20251201`;
- provider `deepinfra`;
- reasoning omitted;
- temperature and seed unchanged;
- 80-token output cap unchanged;
- all 1,032 scientific prompts and hashes unchanged;
- response schema and semantic validation unchanged;
- hypotheses, estimands, exclusions, and analysis plan unchanged.

The unrecovered first-attempt DeepSeek expenditure is excluded from the scientific dataset but included in project-level expenditure accounting.

## Outcome blindness

The repair is motivated solely by a JSON syntax error in the execution log. No scientific output value from DeepSeek or any other model was inspected to specify this amendment.
