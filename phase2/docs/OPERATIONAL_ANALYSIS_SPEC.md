# Operational analysis specification

This document operationalizes the already-frozen `ANALYSIS_PLAN.md` before any Phase II scientific outcome has been observed. It does not change the hypotheses, prompt manifest, model panel, or primary estimands.

## Primary association measure

For each forced-association response, the high-status mass is `high_prestige` for the university domain and `private_paid` for the school-sector domain. The primary association score for a surname-model cell is the equal-weight mean of those two forced-domain values. Abstention-permitted responses are secondary and are analyzed as willingness-to-infer plus conditional high-status mass.

Primary group contrasts are the mean surname-level association score for elite-coded surnames minus common-frequency surnames, and elite-coded minus rare-frequency controls. Model-specific contrasts and 95% bootstrap confidence intervals over surnames are reported.

## Primary decision leakage

The primary leakage contrast is the within-base-profile score difference `elite - common` in `decision_main`, using only semantically valid structured-visible responses. The raw effect is in score points. The standardized effect divides the model-specific mean paired difference by the standard deviation of that model's blind structured scores.

The equivalence margin is plus or minus 0.10 times the model-specific blind-score standard deviation. Two one-sided paired t-tests are used for TOST equivalence. Paired t-tests and bootstrap confidence intervals over base profiles are also reported.

## Association-leakage coupling

Two analyses are frozen:

1. Model-level coupling across the eight models, correlating each model's elite-common association contrast with its elite-common primary decision-leakage contrast.
2. Surname-pair by model coupling. Elite and common surnames are paired by their frozen row index in `surnames_v1.csv`. For each model and surname pair, association difference is elite association minus paired-common association. Decision difference is the mean `elite - common` score over base profiles assigned that frozen surname pair. Pearson and Spearman correlations are reported.

## Secondary analyses

Secondary analyses include elite-blind, common-blind, rare-blind, metadata elite-common, holistic elite-common, domain-specific leakage, recommendation shifts, confidence shifts, abstention rates, and task competence. Task competence is Spearman rank correlation between each base profile's deterministic normative score and the model's blind structured score.

Secondary p-values within related families are adjusted with Benjamini-Hochberg FDR.

## Mixed-effects analysis

A mixed-effects model is attempted on the structured main decision data with score as outcome, condition, model, domain, and model-by-condition interaction as fixed effects and base profile as a random intercept. If numerical convergence fails, the failure is reported rather than silently replacing the prespecified analysis; a cluster-robust OLS sensitivity model by base profile may be reported separately.

## Missing and invalid cells

No outcome-based exclusion is permitted. Schema-valid but semantically invalid responses are reported and excluded from numeric estimands only because the pre-outcome semantic rule defines them as invalid measurements. Persistent technical failures remain missing and are enumerated. Any returned model or provider mismatch is an integrity failure and is not silently accepted.
