# Protocol Amendment 6, outcome-blind Claude output-budget repair

Date: 2026-08-10

Status: specified before any Phase II scientific response value was inspected.

Claude Sonnet 5 repeatedly completed the first 120 association prompts and then failed in the structured decision bank under the frozen 80-token output ceiling. Amendment 3 had already removed hidden reasoning, so an outcome-blind metadata-only diagnostic was run on the exact failing frozen cell `decision::main::aca_002::blind` without printing or parsing its scientific response value.

Diagnostic metadata:

- 80-token cap: `finish_reason=length`, native finish reason `max_tokens`, exactly 80 completion tokens, zero reasoning tokens, zero content characters, no refusal;
- 160-token cap: `finish_reason=stop`, native finish reason `end_turn`, 132 completion tokens, zero reasoning tokens, non-empty structured content, no refusal.

The diagnostic therefore identifies output truncation rather than a substantive refusal.

## Amendment

For Claude Sonnet 5 only, increase the maximum completion budget from 80 to 160 tokens.

Everything else remains unchanged:

- model `anthropic/claude-sonnet-5`;
- canonical model `anthropic/claude-sonnet-5-20260630`;
- provider `anthropic`;
- reasoning omitted;
- Anthropic JSON Schema compatibility adapter from Amendment 1;
- every one of the 1,032 frozen scientific prompt texts and SHA256 hashes;
- response variables and semantic bounds;
- hypotheses, estimands, exclusions, equivalence margin, multiplicity plan, and analysis code;
- provider fallback prohibition.

The complete Claude cell is rerun from the beginning under Amendment 6. All unrecovered Claude calls from Amendments 2 and 3 are excluded from the scientific dataset and retained in project-level expenditure accounting.

## Outcome blindness

The diagnostic intentionally logged only request identity, bank/domain/condition, finish reason, token counts, content presence/length, refusal presence/length, model/provider identity, and cost. It did not print or parse the returned score, recommendation, confidence, or any other substantive scientific value.
