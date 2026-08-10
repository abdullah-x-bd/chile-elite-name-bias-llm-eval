# Protocol Amendment 9: retry one semantic-invalid Mistral abstention cell

**Date:** 2026-08-10

## Status

Outcome-blind execution amendment. No substantive value from the affected response, or from the completed Phase II primary outcomes, was inspected in deciding this amendment.

## Affected cell

Exactly one frozen prompt:

`assoc::common_frequency::flores::school_sector::1`

Model/provider cell:

- model: `mistralai/mistral-medium-3-5`
- canonical model: `mistralai/mistral-medium-3.5-20260430`
- provider: `mistral`

## Reason

The final 8,256-row release verifier found exactly one semantic-contract failure. The response was syntactically valid structured output, but the abstention instrument returned `can_infer=false` while also returning nonzero category probabilities. The pre-frozen semantic contract requires all probabilities to be zero when the model abstains. The actual probability values were not inspected.

The response is therefore unusable under the protocol in the same sense as malformed JSON or a structured response outside the declared schema. The primary verifier correctly rejected the full release rather than silently coercing the values.

## Amendment

For the single affected Mistral prompt only:

- keep the original frozen prompt byte-identical;
- keep the frozen model, canonical model, Mistral provider, schema, temperature/seed/reasoning settings, and output limit unchanged;
- if the structured response fails the pre-frozen semantic validator, retry the identical request up to the existing retry limit;
- accept the first response that satisfies the original frozen semantic contract;
- replace only the unusable original observation in the assembled primary dataset.

No other primary observation is rerun or replaced.

## Scientific interpretation

This amendment does not choose among valid scientific outcomes and does not redefine abstention after observing the result. It merely enforces a response contract specified before data collection. An abstention with nonzero probabilities is not a valid observation under that contract.

## Outcome blindness

At the time of this amendment, the verifier had exposed only the prompt identity and failure class `abstention_probabilities_not_zero`. The underlying category probabilities and all substantive primary estimates remained uninspected.
