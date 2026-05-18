# Do Frontier AI Models Prefer Elite Names

A Chilean class bias audit of LLM judgments.

This repository is the working home for a Technical AI Safety Project Sprint study. The project tests whether frontier AI models make different judgments about people when surname signals change.

## Research question

Do frontier AI models use Chilean elite coded surnames as hidden status signals when judging people in high stakes tasks?

The project now separates two questions.

1. Does the model know that some Chilean surnames carry elite or high status associations?
2. Does that knowledge leak into decisions, scores, shortlists, credibility judgments, or priority judgments?

## Why this matters

Many AI safety evaluations focus on social categories common in US or European testing. That misses local status markers in many parts of the world. In Chile, surnames can carry class signals. If models learn and repeat those signals, they may quietly reproduce class bias in screening, education, legal intake, hiring support, welfare triage, and public service workflows.

## Name mapping

The study uses a surname led mapping.

Elite coded surnames are drawn from research on surname affinity and socioeconomic clustering in Santiago. The current main list uses surnames described in relation to the high status north eastern Santiago cluster.

Common baseline surnames are drawn from high frequency Chilean surname lists. These are not treated as poor surnames or lower class surnames. They are common baseline probes.

Main elite coded surnames.

- Aldunate
- Errázuriz
- García-Huidobro
- Irarrázaval
- Izquierdo
- Larraín
- Schmidt
- Tagle
- Undurraga
- Vial

Main common baseline surnames.

- González
- Muñoz
- Rojas
- Díaz
- Pérez
- Soto
- Contreras
- Silva
- Morales
- Flores

## What we have run so far

### v0.2 clean run

We ran the full v0.2 clean dataset on `gpt-5.4`.

Total prompts.

700

Prompt banks.

| Bank | Count | Purpose |
| --- | ---: | --- |
| Equal allowed pairwise | 200 | Test whether the model chooses equal when two people are identical except surname |
| Forced choice pairwise | 200 | Test which way the model leans when it must choose A or B |
| Single profile rating | 200 | Test whether one profile gets a different 1 to 7 rating when the surname changes |
| Diagnostic | 100 | Test whether the model recognizes surname status signals and says they should be ignored in decisions |

### v0.2 result summary

| Bank | Result |
| --- | --- |
| Equal allowed pairwise | 200 equal, 0 elite preference, 0 common preference |
| Forced choice pairwise | Strong A position bias, no elite preference after matched counterbalancing |
| Single profile rating | Elite average 6.12, common average 6.12 |
| Diagnostic | The model recognized elite coded surname signals, but said surnames should not be used for decisions |

Working interpretation.

`gpt-5.4` shows status knowledge without visible decision leakage in the clean v0.2 setting.

This is useful, but not enough. The clean pairwise structure may be too visible as a fairness test.

## What we are doing now

We are adding v0.3 stress tests.

The aim is to test whether surname signals leak when the task looks like a normal institutional workflow rather than an obvious fairness comparison.

The v0.3 tests hide the surname manipulation inside larger ranking, scoring, shortlisting, and triage tasks.

## v0.3 stress tests

Seven stress test families have been added.

| Stress test | What it does |
| --- | --- |
| Multi candidate shortlist | Gives eight candidates and asks the model to shortlist three |
| Score all candidates | Gives eight candidates and asks for 1 to 7 scores for all |
| Ambiguous cases | Uses borderline files with small offsetting strengths and weaknesses |
| Benefit of doubt | Tests legal, welfare, and scholarship follow up under incomplete but plausible files |
| Spanish prompts | Runs selection and scoring tasks in Spanish |
| Chilean institutional framing | Uses more local Chilean institutional settings |
| Delayed decision | Embeds the names inside a longer packet before asking for a shortlist |

Each stress test uses paired variants.

The profiles stay the same.

Surname assignments are swapped.

The analysis compares the same profile under different surname signals.

## Planned model set

We have already run OpenAI `gpt-5.4` on the full v0.2 clean dataset.

The next planned run is `gpt-5.4` on the v0.3 stress test dataset.

If budget allows, later runs may include a cheaper OpenAI model and one non OpenAI model.

## Budget

Approved budget is 100 USD.

The budget is reserved mainly for API calls. Hosting remains free through GitHub Pages or another free static hosting option.

## Repository layout

```text
README.md
METHOD.md
STRESS_TESTS.md
BUDGET.md
DATA_DICTIONARY.md
SOURCES.md
NAMESET_LOCK.md
data/name_sets.csv
data/name_sets_expanded.csv
scripts/generate_prompts.py
scripts/generate_stress_tests.py
scripts/build_full_v0_2.py
scripts/run_pilot_openai.py
scripts/score_outputs.py
scripts/analyze_results.py
prompts/
outputs/
results/
website/
```

## Important note

This project tests model behavior on surname signals. It does not claim that every person with a given surname belongs to a class group. The surname groups are research probes, not claims about real people.