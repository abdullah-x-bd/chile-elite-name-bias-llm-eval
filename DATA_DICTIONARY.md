# Data dictionary

This file explains the planned data files.

## data/name_sets.csv

Name probes used in the study.

| Column | Meaning |
| --- | --- |
| name_id | Stable name ID |
| full_name | Full synthetic name used in prompts |
| first_name | First name |
| surname | Surname |
| group | elite_coded or common |
| gender_presentation | male, female, or neutral if relevant |
| source_note | Short note on why the name is in this set |
| source_url | Source used for the name grouping |
| include_in_pilot | yes or no |

## data/prompt_templates.csv

Prompt templates used to generate paired prompts.

| Column | Meaning |
| --- | --- |
| template_id | Stable template ID |
| task_family | Prompt family |
| scenario | Short scenario label |
| template_text | Prompt text with placeholders |
| correct_answer | Usually equal |
| risk_note | What failure mode the prompt tests |

## prompts/generated_prompts.jsonl

Generated model prompts.

Each line is one prompt.

Expected fields.

| Field | Meaning |
| --- | --- |
| prompt_id | Stable prompt ID |
| base_id | Base pair ID before counterbalancing |
| task_family | Prompt family |
| elite_position | A or B |
| elite_name_id | Name ID for the elite coded name |
| common_name_id | Name ID for the common name |
| prompt_text | Final prompt sent to the model |
| expected_answer | Usually equal |

## outputs

Raw model outputs will be stored here during local runs.

Large raw outputs may not be committed until cleaned.

## results

Cleaned scored outputs and tables will be stored here.

Expected files.

- scored_outputs.csv
- model_summary.csv
- task_family_summary.csv
- status_reason_examples.csv

## website

Static result page files will be stored here.