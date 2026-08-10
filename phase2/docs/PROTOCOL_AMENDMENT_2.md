# Protocol Amendment 2, pre-outcome

Date: 2026-08-10

Status: frozen before any Phase II scientific response was collected.

Protocol Amendment 1 successfully restored Anthropic schema compatibility and replaced the unavailable DeepSeek V4 Flash cell with DeepSeek V3.2 on the pinned DeepInfra endpoint. A second non-study smoke diagnostic showed that DeepSeek V3.2 with `reasoning: low` and the frozen 80-token output cap could spend the output budget on hidden reasoning and return no final `content` field.

Three non-study variants were tested on the same frozen DeepSeek V3.2 / DeepInfra endpoint:

- reasoning disabled, 80 tokens: transient HTTP 429 during the diagnostic;
- reasoning omitted, 80 tokens: valid structured answer with 27 completion tokens and zero reasoning tokens;
- low reasoning, 256 tokens: valid structured answer, but 157 of 168 completion tokens were reasoning tokens.

## Amendment

For the DeepSeek V3.2 cell only, `reasoning` is changed from `low` to `omit`.

Everything else remains unchanged:

- request model `deepseek/deepseek-v3.2`;
- canonical model `deepseek/deepseek-v3.2-20251201`;
- provider `deepinfra`;
- frozen 80-token output cap;
- temperature and seed behavior;
- exact prompts and prompt hashes;
- structured response schemas;
- semantic validation;
- hypotheses and estimands;
- analysis plan;
- provider fallback prohibition;
- scientific call count.

This amendment prevents hidden reasoning from competing with the predeclared structured response budget. It does not alter the response variables or any scientific prompt.

## Outcome blindness

Only technical smoke and diagnostic prompts were used before Amendment 2. No prompt from the 1,032-cell Phase II scientific manifest was sent to any model before this amendment was frozen.
