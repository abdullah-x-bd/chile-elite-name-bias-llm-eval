# Protocol Amendment 8: retry semantic-invalid Claude structured outputs

**Date:** 2026-08-10

## Status

Outcome-blind execution amendment. No substantive Phase II response value was inspected in deciding this amendment.

## Affected cells

Only the missing Claude Sonnet 5 shards 1 and 7. Shards 0, 2, 3, 4, 5, and 6 completed under Amendment 7 and remain untouched.

## Reason

Under Amendment 7, shard 1 completed all 129 requests within its budget but the final pre-frozen semantic validator detected at least one response that did not satisfy the declared response contract. The job therefore correctly refused to publish the shard. The substantive response value and the identity/value of the semantic-invalid observation were not inspected. Shard 7 failed at GitHub checkout before any scientific request was sent.

The existing executor already retries transport errors, empty content, and syntactically invalid JSON with the identical request. Amendment 8 extends the same policy to a semantically invalid structured response: if a syntactically valid object violates the already-frozen semantic contract, the exact same request is retried up to the existing retry limit rather than accepting an invalid observation and failing only after the shard has completed.

## Amendment

For Claude shards 1 and 7 only:

- keep the frozen Claude Sonnet 5 canonical model and Anthropic provider;
- keep Amendment 7's explicit `reasoning={"enabled": false, "exclude": true}`;
- keep `max_tokens=160`;
- keep every prompt, condition, schema, hypothesis, and analysis rule unchanged;
- if `validate_response` returns false, retry the identical request under the existing retry limit;
- publish only rows whose response passes the pre-frozen semantic validator.

## Scientific interpretation

This changes no scientific value rule and does not select among valid outcomes. It enforces the response contract that was frozen before collection. A response is retried solely because it is unusable under that contract, analogous to malformed JSON or missing content.

## Outcome blindness

At freeze time, completed primary-model scientific values and the semantic-invalid Claude value remained uninspected.
