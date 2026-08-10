# Protocol Amendment 7: Claude explicit no-reasoning transport mode

**Date:** 2026-08-10

## Status

Outcome-blind execution amendment. No Phase II scientific response value was inspected in deciding this amendment.

## Affected cell

`claude_sonnet5` on the frozen Anthropic provider endpoint only.

## Reason

Under Amendment 6, Claude Sonnet 5 remained capable of consuming the 160-token completion ceiling without producing final structured content on some decision prompts, despite the model configuration marking reasoning as omitted. The exact failing frozen request was therefore tested in an outcome-blind transport diagnostic that printed only finish reasons, token counts, content length, JSON validity, refusal presence, provider/model identity, and cost. It never printed or parsed the substantive scientific score.

For the exact failing request, the diagnostic observed:

- implicit/omitted reasoning at 160 tokens: truncated, invalid JSON;
- explicit `reasoning.enabled=false` with `exclude=true` at 160 tokens: valid JSON, normal stop, 27 completion tokens, no refusal;
- `reasoning.effort=none` with `exclude=true` at 160 tokens: valid JSON, normal stop, 27 completion tokens, no refusal;
- implicit/omitted reasoning at 384 tokens: valid JSON, but materially more expensive.

The explicit no-reasoning form therefore solves a provider transport/configuration issue without increasing the scientific output ceiling.

## Amendment

For Claude Sonnet 5 only:

- keep the frozen canonical model and Anthropic provider;
- keep every scientific prompt, condition, schema, hypothesis, and analysis rule unchanged;
- keep `max_tokens = 160`;
- send `reasoning = {"enabled": false, "exclude": true}` explicitly in the OpenRouter request payload;
- retain the existing retry and semantic-validation rules.

The model-panel file itself is not rewritten. This is an execution-layer compatibility override whose exact payload becomes part of the Amendment 7 request identity.

## Scientific interpretation

This amendment does not alter the observable response schema or permissible scientific values. It prevents hidden reasoning tokens from consuming the completion budget before the already-frozen structured response can be emitted. It is therefore treated as a transport/execution amendment, not a hypothesis or outcome amendment.

## Outcome blindness

At the time of freezing this amendment, no substantive Phase II response from the affected diagnostic cell, or from any completed model cell, had been inspected for its scientific value.
