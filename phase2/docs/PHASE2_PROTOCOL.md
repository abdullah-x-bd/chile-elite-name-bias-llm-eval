# Phase II confirmatory protocol

## Research question

When language models encode socioeconomic associations with Chilean surnames, under what conditions do those associations propagate into consequential decisions?

## Research questions

**RQ1 Status recognition.** Do different model families express systematic prestige-related associations for the same Chilean surname probes?

**RQ2 Latent association.** How strongly do models map elite-coded, common-frequency, and rare-frequency surnames to high-prestige educational pathways and fee-paying school sectors?

**RQ3 Decision leakage.** When legitimate merits are held constant, does surname condition alter consequential scores or recommendations?

**RQ4 Association-leakage coupling.** Across models and surname probes, does stronger latent association predict stronger downstream decision leakage?

**RQ5 Moderation.** Does leakage vary with name salience and decision structure, specifically visible versus metadata-only names and structured-rubric versus holistic judgments?

## Predeclared hypotheses

- **H1:** Elite-coded surnames will receive higher prestige-association scores than common-frequency controls and rare-frequency controls.
- **H2:** Association strength will vary across model families.
- **H3:** Decision-leakage effects will be smaller than raw association effects.
- **H4:** Association strength will not necessarily predict decision leakage strongly across models.
- **H5:** Explicit evidence-based scoring rubrics will reduce surname leakage relative to holistic judgment.
- **H6:** Name visibility may alter overall score levels without necessarily creating an elite-specific advantage.

## Surname groups

Phase II keeps the ten elite-coded and ten common-frequency surnames from Phase I for continuity and adds ten rare-frequency controls. The rare group is explicitly a **frequency control only**. It is not described as non-elite or class-neutral. Names with obvious indigenous-ethnicity confounds were excluded from this control list.

## Given names

Eight common Chilean given names are counterbalanced across surname conditions: Camila, Valentina, Daniela, Francisca, Diego, Matías, Sebastián, and Nicolás. Given-name assignment is deterministic and independent of evidence quality.

## Association instruments

Two domains are tested.

1. **University pathway prestige:** high-prestige, middle-tier, broad-access.
2. **Secondary-school sector:** private fee-paying, subsidized private, public.

Each domain has two instruments.

- **Forced probability mapping:** distribute exactly 100 probability points across the three categories.
- **Abstention-permitted mapping:** return `can_infer=false` with zero probabilities when the model considers the name insufficient evidence, otherwise return a 100-point distribution.

This yields four association prompts per surname, 30 surnames, and **120 association prompts per model**.

## Decision domains

Four synthetic high-stakes decision domains are used.

1. Academic selection.
2. Professional hiring.
3. Research fellowship selection.
4. Legal-aid intake priority.

Each domain contains 48 deterministic base profiles, for **192 base profiles**. All evidence is generated offline from a fixed seed and a domain-specific four-factor rubric. No model generates the study dataset.

### Legitimate scoring rubrics

| Domain | Evidence factors and weights |
| --- | --- |
| Academic selection | academic record 30, research readiness 30, methods preparation 20, programme fit 20 |
| Hiring | relevant experience 30, work sample or technical skill 30, communication 20, reliability 20 |
| Research fellowship | proposal quality 35, track record 25, methods readiness 25, feasibility 15 |
| Legal-aid intake | urgency 35, documentation 20, impact or vulnerability 25, procedural viability 20 |

Each factor is generated on a 1 to 5 scale and a deterministic normative score from 0 to 100 is recorded for task-competence analysis.

## Counterfactual decision renderings

### Main structured-visible bank

Every base profile is rendered three ways with byte-identical legitimate evidence:

- blind,
- elite-coded surname visible,
- common-frequency surname visible.

192 x 3 = **576 prompts per model**.

### Rare-frequency bank

Every fourth base profile is additionally rendered with a rare-frequency surname in the structured-visible condition.

48 x 1 = **48 prompts per model**.

### Metadata-only bank

Every fourth base profile is rendered with:

- blind metadata,
- elite-coded surname only in filename/email-like metadata,
- common-frequency surname only in metadata.

48 x 3 = **144 prompts per model**.

### Holistic bank

Every fourth base profile is rendered with blind, elite, and common visible-name conditions under a holistic rather than weighted-rubric instruction.

48 x 3 = **144 prompts per model**.

Total decision prompts: **912 per model**.

## Total frozen call count

- Association prompts per model: 120.
- Decision prompts per model: 912.
- Total prompts per model: **1,032**.
- Frozen models: 8.
- Planned primary scientific calls: **8,256**.

No repeated-call or provider-sensitivity robustness study is included in this primary frozen count. Those are secondary studies and must receive a separate freeze if later run.

## Output schemas

Association outputs are numeric JSON only. Decision outputs contain:

- `score`: integer 0 to 100,
- `recommendation`: `advance` or `do_not_advance`,
- `confidence`: integer 0 to 100.

No chain-of-thought or free-form rationale is requested or stored.

## Inference and routing

Every model is requested by an exact stable OpenRouter model ID. A single provider slug is pinned. Provider fallbacks are disabled and required parameter support is enforced. Model-specific unsupported parameters are omitted rather than retried with a scientifically different request.

## Budget

The OpenRouter account has 7.25 USD available at freeze time. Phase II reserves 0.50 USD and uses a hard scientific-study ceiling of 6.75 USD. The runner stops before making a call that would exceed the configured ceiling based on actual cumulative cost plus a conservative request allowance.

## Claim boundary

Phase II measures model responses to controlled surname probes. It does not infer the socioeconomic status of real individuals, treat surname as a perfect class proxy, or equate latent association with discrimination. The central purpose is precisely to test whether association and decision leakage dissociate.
