# Phase II results

Primary confirmatory dataset: **8,256 model responses** across 8 frozen model/provider endpoints.
Recorded accepted-release OpenRouter cost: **$3.0807**.
Semantically invalid primary rows: **0**.

## Primary latent association

- `claude_sonnet5`: elite-common **+53.60** points, 95% bootstrap CI [+44.85, +60.35], p=7.98e-08.
- `deepseek_v32`: elite-common **+10.00** points, 95% bootstrap CI [+5.75, +14.75], p=0.00156.
- `gemini36flash`: elite-common **+62.10** points, 95% bootstrap CI [+58.55, +65.50], p=8.43e-15.
- `gpt54mini`: elite-common **+40.80** points, 95% bootstrap CI [+28.20, +52.35], p=0.000114.
- `gpt54nano`: elite-common **+6.00** points, 95% bootstrap CI [-0.20, +12.05], p=0.0829.
- `llama4_maverick`: elite-common **+7.00** points, 95% bootstrap CI [+3.50, +10.50], p=0.00442.
- `mistral_medium35`: elite-common **+41.75** points, 95% bootstrap CI [+30.00, +51.50], p=5.94e-05.
- `qwen37max`: elite-common **+36.85** points, 95% bootstrap CI [+26.85, +46.00], p=3.93e-05.

All eight models produced positive elite-minus-rare association contrasts; all eight were conventionally significant at p<0.05.

## Primary decision leakage

- `claude_sonnet5`: elite-common **+0.052** score points, 95% bootstrap CI [-0.375, +0.526], standardized +0.002; equivalence within ±0.10 SD: **yes**.
- `deepseek_v32`: elite-common **-0.026** score points, 95% bootstrap CI [-0.057, +0.005], standardized -0.021; equivalence within ±0.10 SD: **yes**.
- `gemini36flash`: elite-common **-0.010** score points, 95% bootstrap CI [-0.349, +0.323], standardized -0.000; equivalence within ±0.10 SD: **yes**.
- `gpt54mini`: elite-common **-1.365** score points, 95% bootstrap CI [-4.057, +1.120], standardized -0.049; equivalence within ±0.10 SD: **no**.
- `gpt54nano`: elite-common **-1.266** score points, 95% bootstrap CI [-6.901, +4.443], standardized -0.034; equivalence within ±0.10 SD: **no**.
- `llama4_maverick`: elite-common **+0.146** score points, 95% bootstrap CI [+0.010, +0.286], standardized +0.095; equivalence within ±0.10 SD: **no**.
- `mistral_medium35`: elite-common **-0.068** score points, 95% bootstrap CI [-0.656, +0.443], standardized -0.002; equivalence within ±0.10 SD: **yes**.
- `qwen37max`: elite-common **+0.536** score points, 95% bootstrap CI [-0.891, +1.927], standardized +0.031; equivalence within ±0.10 SD: **yes**.

## Association-leakage coupling

Across models: Pearson r=+0.201 (p=0.633); Spearman rho=+0.071 (p=0.867).
Across frozen surname-pair × model cells: Pearson r=+0.065 (p=0.565); Spearman rho=-0.077 (p=0.495).

## Secondary decision evidence

After Benjamini-Hochberg correction, the only secondary contrasts below FDR 0.05 were for Qwen 3.7 Max and compared surname-bearing conditions with the blind condition: elite -2.74 points, common -3.28, and rare -5.81. Because the reduction appears across surname groups, this is a general name-presence effect rather than evidence of elite-specific leakage. No metadata or holistic elite-minus-common contrast survived FDR correction.

## Robustness disposition

The 1,300-call robustness layer was predeclared before outcome inspection, but its frozen budget gate failed after primary execution and documented repair expenditure. Under the preregistered rule, it was left **unexecuted rather than reduced post hoc**.

## Claim boundary

Phase II distinguishes measured surname-status association from consequential decision leakage. A strong association result is not itself evidence of discriminatory decision behavior. Null or equivalent decision effects apply only to the frozen tasks, models, providers, language, and evaluation conditions in this release.
