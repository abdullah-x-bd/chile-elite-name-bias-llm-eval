# Association and Decision Leakage in Large Language Models

A cross-model audit of Chilean surname status signals.

## Status

**Phase II primary study complete.**

- 8 frozen model/provider cells
- 1,032 prompts per model
- **8,256 verified primary responses**
- 192 deterministic matched decision profiles
- 30 surname probes across elite-coded, common-frequency, and rare-frequency controls
- four consequential decision domains
- two latent-association domains
- exact provider pinning and prompt hashes
- pre-outcome protocol and analysis freezes
- final release verifier: **PASS**
- semantically invalid rows in accepted release: **0**

The historical exploratory study is preserved separately as Phase I. The pre-Phase-II state is frozen at commit `feceba1fabbc8ba74d0bc55ca0ed6317a3a44bf0` and branch `archive/phase1-v0.6`.

## Main finding

**Large latent socioeconomic associations do not reliably predict consequential decision leakage.**

Seven of eight evaluated models assigned significantly greater forced high-status probability mass to elite-coded Chilean surnames than to common-frequency surnames. All eight produced positive and statistically detectable elite-minus-rare association contrasts.

Those associations mostly disappeared in matched decisions where legitimate evidence was held constant. Five of eight models were statistically equivalent within a predeclared ±0.10 SD decision-effect margin. Two additional models were inconclusive because their decision estimates were too noisy to establish equivalence. Llama 4 Maverick produced a small nominal elite-common effect of +0.146 score points, or +0.095 SD, close to the practical-equivalence boundary.

Most importantly, association strength did not predict decision leakage:

- model level Pearson `r = 0.201`, `p = 0.633`
- model level Spearman `rho = 0.071`, `p = 0.867`
- surname-pair × model Pearson `r = 0.065`, `p = 0.565`
- surname-pair × model Spearman `rho = -0.077`, `p = 0.495`

The project therefore treats **status recognition, latent association, and consequential treatment as distinct constructs** rather than using an association probe as evidence of discriminatory decision behavior.

## Primary results

| Model | Elite − common association | Elite − common decision | Standardized decision | Equivalent within ±0.10 SD |
| --- | ---: | ---: | ---: | --- |
| Claude Sonnet 5 | +53.60 | +0.052 | +0.002 | Yes |
| DeepSeek V3.2 | +10.00 | -0.026 | -0.021 | Yes |
| Gemini 3.6 Flash | +62.10 | -0.010 | -0.000 | Yes |
| GPT-5.4 Mini | +40.80 | -1.365 | -0.049 | No, imprecise |
| GPT-5.4 Nano | +6.00 | -1.266 | -0.034 | No, imprecise |
| Llama 4 Maverick | +7.00 | +0.146 | +0.095 | No, borderline |
| Mistral Medium 3.5 | +41.75 | -0.068 | -0.002 | Yes |
| Qwen 3.7 Max | +36.85 | +0.536 | +0.031 | Yes |

Association values are high-status probability points from the frozen forced-association instrument. Decision values are paired score-point differences over identical underlying profiles.

See [`phase2/results/RESULTS.md`](phase2/results/RESULTS.md) for confidence intervals, p-values, claim boundaries, and secondary findings.

## Why the rarity control matters

The project does not treat common surnames as a proxy for low socioeconomic status. Phase II adds a third group of **rare-frequency controls** to test whether unusual surname form or rarity alone explains the association signal.

Elite-coded surnames received more high-status probability mass than rare-frequency controls in all eight models. The strongest association results therefore cannot be reduced to a simple common-versus-uncommon surname distinction.

## Decision design

Phase II uses 192 deterministic synthetic evidence profiles across:

- academic selection
- professional hiring
- research fellowship selection
- legal-aid intake

For the primary bank, each base profile is rendered into matched blind, elite-coded, and common-frequency conditions. Legitimate evidence is identical across the counterfactual versions.

Additional frozen banks test:

- rare-frequency surnames
- names visible only in metadata
- holistic rather than explicitly weighted decision instructions

After false-discovery-rate correction, no metadata or holistic elite-minus-common contrast remained significant. The only surviving secondary effects were for Qwen 3.7 Max, where elite, common, and rare surname-bearing profiles all scored below blind versions. That pattern is more consistent with a general name-presence effect than elite-specific leakage.

## Association instruments

Association is measured separately from decisions in two Chile-specific domains:

- university prestige
- secondary-school sector

Each is evaluated twice.

**Forced association** requires exactly 100 probability points across ordered status outcomes.

**Abstention-permitted association** lets a model state that surname alone is insufficient for inference.

This distinction exposes major model differences in willingness to operationalize social knowledge. Some systems express elite-status inferences when abstention is allowed, while others abstain across nearly every surname group. The primary cross-model association estimand therefore uses the common forced instrument.

## Model panel

The accepted primary release contains these exact model/provider cells:

| Label | Requested model | Provider |
| --- | --- | --- |
| `gpt54mini` | `openai/gpt-5.4-mini` | OpenAI |
| `gpt54nano` | `openai/gpt-5.4-nano` | OpenAI |
| `claude_sonnet5` | `anthropic/claude-sonnet-5` | Anthropic |
| `gemini36flash` | `google/gemini-3.6-flash` | Google AI Studio |
| `deepseek_v32` | `deepseek/deepseek-v3.2` | DeepInfra |
| `qwen37max` | `qwen/qwen3.7-max` | Alibaba |
| `mistral_medium35` | `mistralai/mistral-medium-3-5` | Mistral |
| `llama4_maverick` | `meta-llama/llama-4-maverick` | DeepInfra |

Provider fallbacks were disabled. The experiment records requested model, canonical model, provider, prompt hash, structured response, usage, cost, latency, and retry state.

## Protocol integrity

Phase II was separated from the exploratory study before the multi-model run. The protocol, deterministic profile generator, analysis plan, model/provider panel, and 1,032-cell-per-model manifest were cryptographically fingerprinted before scientific execution.

The primary manifest digest is:

`280bf06a20a2a3d346340a1d22d4496027c1cda574601121685fc0e37efdb2ff`

Execution problems were handled through documented amendments rather than silently changing the study. These include provider/schema compatibility, replacement of an unavailable pre-run DeepSeek endpoint, response-budget compatibility, exact-request retry for malformed or semantic-invalid structured output, and one final single-cell Mistral response-contract repair. No substantive primary outcome was inspected while those amendments were being decided.

See `phase2/docs/PROTOCOL_AMENDMENT_*.md` and `phase2/freeze/` for the audit trail.

## Verification

The final verifier reports:

```json
{
  "status": "PASS",
  "rows": 8256,
  "expected_rows": 8256,
  "unique_request_identities": 8256,
  "total_cost_usd": 3.080652,
  "failures": []
}
```

The accepted scientific rows cost $3.0807. Total OpenRouter key expenditure was higher because the audit deliberately retains the cost of diagnostics, discarded partial execution attempts, and compatibility repairs.

The machine-readable certificate is at [`phase2/results/PRIMARY_VERIFICATION.json`](phase2/results/PRIMARY_VERIFICATION.json).

## Robustness status

A 1,300-call robustness layer was frozen before outcome inspection. It specified repeated-run stability, an English context-shift subset, and a second-provider DeepSeek check.

It was **not executed**. The preregistered protocol required live usage plus a conservative $0.80 robustness allowance to remain below a $6.75 project ceiling. Primary execution and documented repair expenditure exhausted that envelope. The protocol explicitly prohibited shrinking the robustness subset after observing primary outcomes, so the study records the layer as predeclared but unexecuted.

See [`phase2/results/robustness_disposition.json`](phase2/results/robustness_disposition.json).

## Reproduce the analysis

The primary analysis is deterministic once the accepted raw response ledgers are present under `phase2/results/raw/`.

```bash
cd phase2
python scripts/verify_primary.py
python scripts/analyze_results.py
```

The verifier must pass before the generated statistics or figures are treated as release results.

The analysis produces:

- model-level association contrasts
- elite-common decision leakage estimates
- bootstrap confidence intervals
- equivalence tests using the frozen ±0.10 SD margin
- association-leakage coupling
- secondary FDR-adjusted contrasts
- abstention summaries
- task-competence metrics
- mixed-effects analysis
- eight publication figures

## Manuscript

A paper-ready LaTeX manuscript is under [`phase2/paper/`](phase2/paper/).

Working title:

**Association and Decision Leakage in Large Language Models: A Cross Model Audit of Chilean Surname Status Signals**

The manuscript treats Chile as a controlled culturally specific case study for a broader evaluation problem: **latent social association is not the same construct as consequential decision behavior**.

## Phase I

Phase I remains available for provenance and hypothesis-generation history. It contains 5,180 earlier GPT-family prompts, including the original institution-prestige mapping result, large academic replication, and hidden-metadata study.

Those exploratory results are not pooled into Phase II confirmatory estimates.

## Scope

Surnames are experimental probes, not labels of an individual's socioeconomic status. The rare-frequency set is a rarity control, not a socioeconomic control group. All decision profiles are synthetic. Results apply to the frozen prompts, model versions, providers, Chilean-Spanish context, and decision structures tested here.

A strong association finding should not be read as evidence that a model discriminates in consequential decisions. Likewise, a small or equivalent average decision effect in this benchmark does not establish absence of discrimination in every deployment context.
