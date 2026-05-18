# Do Frontier AI Models Prefer Elite Names

A Chilean class bias audit of LLM judgments.

This repository is the working home for a Technical AI Safety Project Sprint study. The project tests whether frontier AI models use Chilean elite coded surnames as hidden status signals when judging people in high stakes tasks.

## Research question

Do frontier AI models know that some Chilean surnames carry elite status associations, and does that knowledge leak into decisions, scores, credibility judgments, priority judgments, or institutional mappings?

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

## Results so far

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

### Chilean institutional framing v0.3

Model.

`gpt-5.4-mini`

Total prompts.

680

| Bank | Result |
| --- | --- |
| Institutional pairwise equal | 197 igual, 2 elite preferences, 1 common preference |
| Institutional pairwise forced | 101 elite choices, 99 common choices after matching |
| Institutional single profile rating | Elite average 4.27, common average 4.07 |
| Institutional diagnostic | Strong diagnostic recognition of elite coded surnames, but decision-use prompts still said no or ignore for merit |

The single-profile rating gap was concentrated in academic selection, but that signal did not survive the focused replication below.

| Task family | Elite avg | Common avg | Difference |
| --- | ---: | ---: | ---: |
| Academic selection | 5.69 | 4.59 | +1.10 |
| Hiring | 4.00 | 4.00 | 0.00 |
| Legal credibility | 4.00 | 4.00 | 0.00 |
| Policy fellowship | 4.00 | 4.00 | 0.00 |
| Public service | 4.00 | 3.81 | +0.19 |
| Scholarship selection | 4.00 | 4.00 | 0.00 |

### Institution prestige mapping v0.4

Model.

`gpt-5.4-mini`

Total prompts.

600

This run treats institution mapping as one more signal. It asks whether the model maps Chilean names to high-prestige or broad-access education pathways.

| Bank | Result |
| --- | --- |
| Choice | High-prestige ceiling effect. Every name was mapped to a high-prestige institution |
| Probability distribution | Elite-coded surnames received 72.59 high-prestige probability mass, common baseline received 55.97 |
| Tier choice | The model chose cannot infer from name for all 200 prompts |

The cleanest result is the probability distribution arm.

| Group | Avg high-prestige probability mass | Avg broad-access probability mass |
| --- | ---: | ---: |
| Elite coded surnames | 72.59 | 27.41 |
| Common baseline surnames | 55.97 | 44.03 |

Difference.

| Metric | Value |
| --- | ---: |
| Elite minus common high-prestige mass | +16.62 points |
| Welch t-test | p around 1.6e-30 |
| Mann-Whitney | p around 1.5e-23 |

Choice prompt split inside high-prestige institutions.

| Group | PUC Chile | Universidad de Chile | Universidad de los Andes |
| --- | ---: | ---: | ---: |
| Elite coded surnames | 87 | 10 | 3 |
| Common baseline surnames | 0 | 100 | 0 |

Working interpretation.

This is not a decision bias result. It is a strong institutional mapping result. The model refuses explicit tier inference when allowed to say cannot infer, but it reveals a strong surname-to-institution association in probability mapping.

### Academic focused replication v0.5

Model.

`gpt-5.4-mini`

Total prompts.

2000

This run tested whether the academic-selection signal from institutional framing repeats with a much larger single-profile academic dataset.

| Group | Count | Average rating |
| --- | ---: | ---: |
| Elite coded | 1000 | 6.420 |
| Common baseline | 1000 | 6.418 |

Difference.

| Metric | Value |
| --- | ---: |
| Elite minus common | +0.002 |
| Welch t-test | p = 0.928 |
| Mann-Whitney | p = 0.928 |
| Cohen's d | 0.004 |

Working interpretation.

The academic-selection gap did not replicate. The earlier institutional academic signal should now be treated as small-sample or prompt-context noise.

### Hidden metadata academic review v0.6

Model.

`gpt-5.4-mini`

Total prompts.

500

Candidate-level scored records.

6000

This run hid names inside PDF filenames and email sender metadata. It was designed to look less like a fairness test.

| Condition | Main result |
| --- | --- |
| File metadata matched test | Elite minus common score +0.005, p = 0.584 |
| Email metadata matched test | Elite minus common score -0.004, p = 0.684 |
| Shortlist selection | Elite 25.0 percent, common 25.0 percent in both file and email modes |
| High-mapping elite surnames | No stable advantage |

Name visibility made the model slightly more generous, but not in an elite-specific way.

| Condition | Average score | Change from blind |
| --- | ---: | ---: |
| blind_file | 5.269 | 0.000 |
| file_named | 5.385 | +0.116 |
| file_swapped | 5.413 | +0.144 |
| email_named | 5.348 | +0.079 |
| email_swapped | 5.334 | +0.065 |

Working interpretation.

This was the strongest hidden decision test so far. It still did not show elite-name decision leakage. The model mostly used evidence strength, not surname group.

## Current interpretation

The strongest current story is:

- The model knows Chilean elite-coded surname signals.
- Chilean Spanish makes that recognition cleaner.
- Obvious fairness prompts mostly suppress the signal.
- Institution prestige mapping shows a strong hidden surname-to-education pathway association.
- Academic decision leakage is not supported by the focused replication.
- Hidden metadata academic review also did not show stable elite-surname decision leakage.

## Discussion notes

The working notes, full tables, rough comments, and planned graphs are in:

`DISCUSSION.md`

## What we are doing next

The current positive finding is institution prestige mapping.

The current negative finding is that academic decision leakage did not replicate in focused or hidden metadata review tasks.

Next work should either deepen the institution mapping arm or test another hidden association pathway without claiming decision bias too early.

## Budget

Approved budget is 100 USD.

The budget is reserved mainly for API calls. Hosting remains free through GitHub Pages or another free static hosting option.

## Repository layout

```text
README.md
METHOD.md
DISCUSSION.md
INSTITUTIONAL_FRAMING.md
INSTITUTION_PRESTIGE_MAPPING.md
ACADEMIC_FOCUSED_REPLICATION.md
HIDDEN_METADATA_ACADEMIC_REVIEW.md
BUDGET.md
DATA_DICTIONARY.md
SOURCES.md
NAMESET_LOCK.md
data/name_sets.csv
data/name_sets_expanded.csv
data/institution_tiers_chile.csv
scripts/generate_prompts.py
scripts/generate_chilean_spanish_full_v0_2.py
scripts/generate_chilean_institutional_framing_v0_3.py
scripts/generate_institution_prestige_mapping_v0_4.py
scripts/generate_academic_focused_single_profile_v0_5.py
scripts/generate_hidden_metadata_academic_review_v0_6.py
scripts/run_pilot_openai.py
prompts/
outputs/
results/
website/
```

## Important note

This project tests model behavior on surname signals. It does not claim that every person with a given surname belongs to a class group. The surname groups are research probes, not claims about real people.