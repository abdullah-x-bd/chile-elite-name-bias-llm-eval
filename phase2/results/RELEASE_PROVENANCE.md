# Phase II release provenance

## Final verified primary release

The accepted Phase II primary dataset contains exactly **8,256 semantically valid responses**, with **1,032 responses from each of eight frozen model/provider cells**.

The final release verifier certificate is `PRIMARY_VERIFICATION.json` and records:

- status: `PASS`
- expected rows: 8,256
- observed rows: 8,256
- unique request identities: 8,256
- verifier failures: 0
- accepted scientific-row cost: USD 3.080652

## Final verification workflow

The successful final verification and analysis workflow was GitHub Actions run:

`31408624080`

The uploaded final verified research artifact was:

- artifact name: `chile-phase2-final-verified`
- artifact ID: `9070672447`
- artifact ZIP SHA256: `3fa9e991dec98cb4a1b4e60366b13108bbe467925a48a035b68a085c044a93aa`

The artifact contains the complete API-level accepted ledgers, generated statistics, figures, cost records, and verifier outputs used for the primary analysis.

## Source runs used in the final assembly

The final dataset was reconstructed from immutable successful artifacts rather than repeatedly purchasing all model cells.

- Original complete model cells: Actions run `31397776217`
  - GPT-5.4 Mini
  - Gemini 3.6 Flash
  - Qwen 3.7 Max
  - Mistral Medium 3.5
  - Llama 4 Maverick
- Completed GPT-5.4 Nano and DeepSeek repair shards: run `31403135308`
- Successful Claude Amendment 7 shards 0, 2, 3, 4, 5, and 6: run `31405985125`
- Claude Amendment 8 shards 1 and 7: run `31407489803`
- Single-cell Mistral Amendment 9 repair and final verifier/analysis: run `31408624080`

No completed valid model cell was intentionally repurchased during final recombination.

## Execution amendments

All post-freeze execution changes are documented individually under `phase2/docs/PROTOCOL_AMENDMENT_*.md` and bound by amendment fingerprints under `phase2/freeze/`.

The amendments cover provider/schema compatibility, replacement of an unavailable pre-run DeepSeek endpoint, output-budget compatibility, explicit no-reasoning transport configuration for Claude, identical-request retries for malformed or semantic-invalid structured outputs, and one final single-cell Mistral response-contract repair.

No substantive primary response value was inspected while these execution amendments were chosen. The final statistical analysis was unlocked only after the 8,256-row verifier passed.

## Cost accounting

`phase2/results/tables/cost_ledger.csv` reports costs for the accepted scientific rows only. These sum to USD 3.08065237.

Actual OpenRouter key usage after the final primary collection was USD 7.09970498 because it additionally includes smoke tests, outcome-blind diagnostics, discarded partial attempts, and execution-repair calls. Those costs are not silently attributed to the accepted release rows.

## Robustness disposition

A 1,300-call robustness layer was frozen before primary outcomes were inspected. Its preregistered execution rule required live usage plus a conservative USD 0.80 allowance to stay below the USD 6.75 project ceiling.

That condition failed after primary collection and repair expenditure. The robustness layer was therefore recorded as **predeclared but unexecuted** rather than reduced after seeing results. The exact disposition is stored in `robustness_disposition.json`.

## Durable accepted-output archive

GitHub Actions artifacts have finite retention. To preserve the scientific response matrix permanently, `phase2/results/raw_release/` stores a compact deterministic archive containing `prompt_id` and accepted `parsed_response` for every model cell.

`raw_release/MANIFEST.json` records row counts and SHA256 hashes. `scripts/restore_raw_release.py` decodes, decompresses, hash-checks, and validates the archive, and must produce exactly 8,256 accepted outputs.

The compact Git archive is intended for durable scientific reanalysis. The historical Actions artifact above remains the canonical transport-level evidence package for the exact final verifier run.
