# Phase II robustness protocol

Date: 2026-08-10

Status: specified before any Phase II scientific response value was inspected.

The primary confirmatory study remains the sole basis for the four preregistered primary estimands. This robustness layer is secondary and does not alter the primary dataset, hypotheses, equivalence margin, or multiplicity plan.

The robustness layer is deliberately budget-scaled to preserve the original USD 7.25 account ceiling after the primary run and any documented execution-repair expenditure.

## Deterministic 5 percent subset

Exactly 52 of the 1,032 frozen scientific prompts are selected without reference to outcomes. Selection is stratified by primary bank and uses ascending SHA256 of `robustness-v1|prompt_id` within each bank.

Frozen bank allocation:

- association: 6 of 120
- decision_main: 29 of 576
- decision_rare: 2 of 48
- decision_metadata: 7 of 144
- decision_holistic: 8 of 144

Total: 52 prompts.

The same 52 prompt identities are used for every model and every robustness family below.

## R1. Repeated-run stability

Each of the eight final model/provider cells receives two additional independent calls for each of the 52 Spanish prompts, for 832 additional calls.

The scientific prompt text and output schema are byte-identical to the primary version. Request identities add only a robustness replicate index. Model/provider routing follows the final accepted primary execution configuration.

Primary stability summaries:

- decision score absolute deviation across repeats;
- decision recommendation agreement;
- association high-status-mass absolute deviation;
- abstention agreement where applicable.

This is a measurement-stability check and is not pooled into the primary effect estimates.

## R2. English-language context shift

The same 52 scientific cells are rendered in a deterministic English translation that preserves:

- the same underlying synthetic profile;
- surname and given-name treatment;
- visibility or metadata placement;
- legitimate evidence values;
- structured rubric weights;
- forced versus abstention association semantics;
- output schema and numeric ranges.

Each of the eight model/provider cells receives one English call for each selected cell, for 416 additional calls.

The English subset is compared against the corresponding Spanish primary cells. It is a context-shift sensitivity analysis, not a second primary language study.

## R3. Provider sensitivity

DeepSeek V3.2 is rerun on the same 52 Spanish cells using a second predeclared live provider:

- model: `deepseek/deepseek-v3.2`
- canonical model: `deepseek/deepseek-v3.2-20251201`
- primary provider: DeepInfra
- sensitivity provider: StreamLake
- StreamLake endpoint observed before outcome inspection: `streamlake/fp8`

Provider fallbacks remain disabled. The comparison assesses whether the same canonical open-weight model produces materially different measurements across two serving endpoints.

This adds 52 calls.

## Total robustness size

- repeated-run stability: 832
- English subset: 416
- provider sensitivity: 52
- total: 1,300 calls

## Budget gate

Robustness is executed only if the live OpenRouter key usage plus a conservative USD 0.80 robustness allowance remains below USD 6.75. If the budget gate fails, the robustness layer is recorded as predeclared but unexecuted rather than reducing the subset after observing primary outcomes.

## Outcome blindness

The selection algorithm, bank allocation, English rendering rules, second provider, call count, and budget gate were committed before any Phase II scientific response value was downloaded or inspected.
