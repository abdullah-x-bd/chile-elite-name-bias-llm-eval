# Chilean Surname Association and Decision Leakage, Phase II

Phase II is a separate, frozen confirmatory study built beside the historical Phase I work. Phase I remains unchanged and is preserved at commit `feceba1fabbc8ba74d0bc55ca0ed6317a3a44bf0` and branch `archive/phase1-v0.6`.

## Central question

**When language models encode socioeconomic associations with Chilean surnames, under what conditions do those associations propagate into consequential decisions?**

Phase II separates three constructs that Phase I showed should not be conflated:

1. status recognition,
2. latent socioeconomic or prestige association,
3. decision leakage under matched evidence.

The confirmatory study uses eight frozen model endpoints through OpenRouter, three surname groups, two association domains, four decision domains, matched counterfactual profiles, structured and holistic decision modes, visible and metadata-only name exposure, exact prompt hashes, fixed provider routing, resumable execution, and a hard study budget.

## Scientific freeze

No Phase II scientific API calls are part of this foundation commit. The frozen manifest contains **1,032 prompts per model** and the frozen eight-model panel yields **8,256 planned primary calls**.

The only accepted OpenRouter secret name is:

```text
OPENROUTER_API_KEY
```

The key is read from the environment and is never written to logs or committed files.

## Main files

- `docs/PHASE1_FREEZE.md` explains the separation from Phase I.
- `docs/PHASE2_PROTOCOL.md` predeclares research questions, hypotheses, instruments, controls, and call counts.
- `docs/ANALYSIS_PLAN.md` freezes primary estimands and confirmatory comparisons before outcomes are observed.
- `config/models.json` fixes model and provider identities.
- `data/frozen/base_profiles_v1.jsonl` contains deterministic synthetic evidence profiles.
- `data/frozen/prompt_manifest_v1.jsonl.gz.b64` is a deterministic, text-safe compressed archive containing every scientific cell plus its exact pre-outcome prompt hash. Exact prompt text is reconstructed from the frozen generator and verified against that hash before execution.
- `freeze/study_fingerprint.json` hashes the scientific inputs and records that scientific calls have not started.

## Build and verify locally

```bash
cd phase2
python scripts/build_freeze.py --verify
python -m unittest discover -s tests -v
python scripts/verify_freeze.py
python scripts/estimate_cost.py
```

## Run later

After the protocol is merged and the API key is available in the environment:

```bash
export OPENROUTER_API_KEY='...'
python scripts/resolve_models.py --verify-frozen
python scripts/run_confirmatory.py
```

The runner pins the requested provider, disables fallbacks, resumes by deterministic request identity, stores raw and parsed outputs, tracks actual OpenRouter cost, and stops before the configured budget ceiling.

## Scope

This study does not assume that a surname reveals a person's actual class. Surnames are controlled experimental probes. The rare-frequency group is a frequency control, not a claim of socioeconomic neutrality. Phase II tests model behaviour under counterfactual name substitution while keeping legitimate evidence fixed.
