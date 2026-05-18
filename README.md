# Do Frontier AI Models Prefer Elite Names

A Chilean class bias audit of LLM judgments.

This repository is the working home for a Technical AI Safety Project Sprint study. The project tests whether frontier AI models make different judgments about people when all merit related details are held constant and only the Chilean surname changes.

## Research question

When two synthetic people have the same qualifications, same context, and same evidence, do frontier AI models prefer the person with an elite coded Chilean surname over the person with a common Chilean baseline surname?

## Why this matters

Many AI safety evaluations focus on social categories that are common in US or European testing. That misses local status markers in many parts of the world. In Chile, surnames can carry class signals. If models learn and repeat those signals, they may quietly reproduce class bias in high stakes settings.

This matters for AI systems used in screening, education, public service access, legal intake, hiring support, welfare triage, and institutional decision support.

## Core idea

The study uses paired prompts.

Each prompt gives the model two people. The people are identical in all relevant details. The only changed variable is the surname.

The correct answer should usually be equal.

If a model repeatedly prefers elite coded surnames, or gives status based explanations, that becomes a measurable bias signal.

## Name mapping

The main study uses a surname led mapping.

Elite coded surnames are drawn from research on surname affinity and socioeconomic clustering in Santiago. The current main list uses surnames described in relation to the high status north eastern Santiago cluster.

Common baseline surnames are drawn from high frequency Chilean surname lists. These are not treated as poor surnames or lower class surnames. They are common baseline probes.

The main clean test changes surnames while keeping first names neutral and repeated across groups.

## Planned task families

- Academic selection
- Scholarship selection
- Internship and hiring
- Public policy fellowship selection
- Legal credibility
- Public service or welfare credibility

## Planned model set

The first run will use a mix of stronger and cheaper models so the approved budget can support more trials.

- OpenAI frontier model
- OpenAI lower cost model
- Anthropic Sonnet class model
- Anthropic lower cost model
- Google Gemini Pro or Flash model
- One open weight or hosted open model if cost allows

The final model list will be recorded before the main run.

## Planned outputs

- Prompt dataset
- Name set with source notes
- Python scripts for prompt generation, model calls, scoring, and analysis
- Raw or cleaned model outputs
- Summary tables
- Public write up
- Public results webpage through free static hosting

## Budget

Approved budget is 100 USD.

Planned use.

| Item | Amount |
| --- | ---: |
| OpenAI model calls | 35 USD |
| Anthropic model calls | 25 USD |
| Google model calls | 15 USD |
| LLM assisted scoring and checks | 10 USD |
| Reruns, debugging, and failed calls | 10 USD |
| Final result checks | 5 USD |

No paid hosting is planned. The result page will use GitHub Pages or another free static hosting option.

## Main metrics

- Elite preference rate
- Common name preference rate
- Equal answer rate
- Elite preference among unequal answers
- High confidence unequal answer rate
- Status coded explanation rate
- Fairness correction rate

## Current status

Project setup is in progress.

The initial source backed surname map has been added. The next work is to verify the name set once more, lock the prompt templates, run a small pilot, then run the main model comparison.

## Repository layout

```text
README.md
METHOD.md
BUDGET.md
DATA_DICTIONARY.md
SOURCES.md
data/name_sets.csv
data/name_sets_expanded.csv
data/prompt_templates.csv
prompts/generated_prompts.jsonl
scripts/generate_prompts.py
scripts/run_models.py
scripts/score_outputs.py
scripts/analyze_results.py
outputs/
results/
website/
```

## Important note

This project tests model behavior on surname signals. It does not claim that every person with a given surname belongs to a class group. The surname groups are research probes, not claims about real people.