# Frozen analysis plan

This document is part of the Phase II pre-outcome freeze.

## Primary estimands

1. **Elite-common association contrast:** mean high-status probability mass for elite-coded surnames minus common-frequency surnames.
2. **Elite-rare association contrast:** mean high-status probability mass for elite-coded surnames minus rare-frequency controls.
3. **Elite-common decision leakage:** within-profile score difference between elite-visible and common-visible renderings under the primary structured rubric.
4. **Association-leakage coupling:** cross-model and surname-level relationship between measured association strength and matched decision-score shift.

## Primary decision outcome

Continuous decision score on a 0 to 100 scale. Recommendation is a secondary binary outcome. Confidence is descriptive.

## Matched design

All decision effects use within-base-profile counterfactual comparisons. Legitimate evidence remains fixed across blind, elite, common, and where applicable rare surname renderings.

## Primary analyses

- Report effect estimates with 95% confidence intervals, not only p-values.
- Use paired comparisons for matched profile contrasts.
- Report model-specific effects and pooled descriptive summaries.
- Predefine a smallest effect size of interest of **0.10 standard deviations** for continuous decision leakage. TOST equivalence tests will distinguish evidence of a practically small effect from merely failing to reject zero.
- Association-leakage coupling will be reported both across model-level aggregates and across surname-by-model cells where estimable.

## Secondary analyses

- Elite versus blind, common versus blind, and rare versus blind score shifts.
- Visible versus metadata-only moderation.
- Structured-rubric versus holistic moderation.
- Task-domain heterogeneity.
- Task competence, measured by rank agreement between the deterministic normative evidence score and model score.
- Refusal or abstention rates.

## Multiplicity

The four primary estimands above are the confirmatory family. Secondary comparisons will be clearly labelled exploratory/secondary and use Benjamini-Hochberg false-discovery-rate adjustment where multiple related hypotheses are tested.

## Missingness and malformed outputs

API failures are not model responses and are retried only under the exact same request identity. Persistent failures, refusals, abstentions, and schema-invalid responses are recorded separately. No malformed output is silently coerced to a numeric outcome.

## Exclusions

No prompt cell is removed based on observed outcome. Any technical exclusion must be defined by a pre-outcome integrity rule such as duplicate identity, manifest-hash mismatch, wrong returned model/provider, or schema failure and will be reported explicitly.

## Freeze discipline

Primary hypotheses, estimands, prompt manifest, model IDs, provider pins, and schemas are fixed before scientific execution. Any later robustness extension receives a separate version and fingerprint.
