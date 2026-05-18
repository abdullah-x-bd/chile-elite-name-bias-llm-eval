# Do Frontier AI Models Prefer Elite Names

A Chilean class bias audit of LLM judgments.

This repository is the working home for a Technical AI Safety Project Sprint study. The project tests whether frontier AI models use Chilean elite coded surnames as hidden status signals when judging people in high stakes tasks.

## Research question

Do frontier AI models know that some Chilean surnames carry elite status associations, and does that knowledge leak into decisions, scores, credibility judgments, or priority judgments?

## Current language choice

From this stage onward, new runs use Chilean Spanish.

We moved to Chilean Spanish because local language may make Chilean surname signals more salient than English prompts.

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

### English v0.2 clean run

Model.

`gpt-5.4`

Total prompts.

700

| Bank | Result |
| --- | --- |
| Equal allowed pairwise | 200 equal, 0 elite preference, 0 common preference |
| Forced choice pairwise | Strong A position bias, no elite preference after matched counterbalancing |
| Single profile rating | Elite average 6.12, common average 6.12 |
| Diagnostic | Model recognized elite coded surname signals but said surnames should not be used for decisions |

Working interpretation.

The model showed status knowledge without visible decision leakage in the clean English v0.2 setting.

### Chilean Spanish v0.2 clean run

Model.

`gpt-5.4-mini`

Total prompts.

700

We ran this because Chilean Spanish might make the Chilean surname signal stronger.

| Bank | Result |
| --- | --- |
| Equal allowed pairwise | 200 igual, 0 elite preference, 0 common preference |
| Forced choice pairwise | 106 elite choices, 94 common choices, weak and not statistically strong |
| Single profile rating | Elite average 6.05, common average 6.06 |
| Diagnostic | Strong diagnostic recognition of elite coded surnames, but decision-use prompts still said no or ignore for merit |

Working interpretation.

Chilean Spanish increased diagnostic recognition, but did not create visible decision leakage in equal allowed or single profile tasks. Forced choice showed a small elite lean, but the result was weak and still mixed with position bias.

## What we are doing now

We are no longer running all stress tests together.

We will add stress tests one by one.

The first one is Chilean institutional framing.

This keeps the same basic v0.2 structure, but rewrites the prompts as local Chilean institutional workflows in Chilean Spanish.

## Chilean institutional framing v0.3

The institutional framing run includes:

| Bank | Count |
| --- | ---: |
| Institutional pairwise equal | 200 |
| Institutional pairwise forced | 200 |
| Institutional single profile rating | 200 |
| Institutional diagnostic | 80 |

Total prompts.

680

The prompts use settings such as:

- Una universidad chilena con sede en Santiago
- Un comité chileno de becas de políticas públicas
- Una organización chilena que contrata practicantes de análisis
- Un programa chileno de liderazgo cívico
- Una clínica jurídica chilena en Santiago
- Una oficina municipal chilena

Main question.

Does local Chilean institutional framing produce surname decision leakage where clean Chilean Spanish v0.2 did not?

## Budget

Approved budget is 100 USD.

The budget is reserved mainly for API calls. Hosting remains free through GitHub Pages or another free static hosting option.

## Repository layout

```text
README.md
METHOD.md
INSTITUTIONAL_FRAMING.md
BUDGET.md
DATA_DICTIONARY.md
SOURCES.md
NAMESET_LOCK.md
data/name_sets.csv
data/name_sets_expanded.csv
scripts/generate_prompts.py
scripts/generate_chilean_spanish_full_v0_2.py
scripts/generate_chilean_institutional_framing_v0_3.py
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