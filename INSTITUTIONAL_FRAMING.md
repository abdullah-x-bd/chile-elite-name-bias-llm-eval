# Chilean institutional framing v0.3

From this stage onward, new prompt runs use Chilean Spanish as the main language.

## Why this arm exists

The English gpt-5.4 full v0.2 run showed status knowledge without visible decision leakage.

The Chilean Spanish gpt-5.4-mini full v0.2 run was added because local language may make Chilean surname signals more salient.

That Spanish run showed strong diagnostic recognition of elite coded surnames, but still no clear surname effect in equal allowed decisions or single profile ratings. Forced choice showed only a weak elite lean mixed with strong position bias.

The next test is Chilean institutional framing.

The aim is to keep the same basic v0.2 structure, but make the task feel more like a local Chilean institutional workflow.

## Prompt banks

The institutional framing run has four banks.

| Bank | Count |
| --- | ---: |
| Institutional pairwise equal | 200 |
| Institutional pairwise forced | 200 |
| Institutional single profile rating | 200 |
| Institutional diagnostic | 80 |

Total prompts.

680

## Settings used

The prompts use Chilean Spanish and local institutional settings such as:

- Una universidad chilena con sede en Santiago
- Un comité chileno de becas de políticas públicas
- Una organización chilena que contrata practicantes de análisis
- Un programa chileno de liderazgo cívico
- Una clínica jurídica chilena en Santiago
- Una oficina municipal chilena

## Core design rule

Only surname signals change.

The model should not use surnames for merit, credibility, or priority decisions.

Pairwise prompts remain counterbalanced so elite coded surnames appear once as A and once as B.

## Generated files

```text
prompts/institutional_pairwise_equal_chilean_spanish_v0_3.jsonl
prompts/institutional_pairwise_forced_chilean_spanish_v0_3.jsonl
prompts/institutional_single_profile_chilean_spanish_v0_3.jsonl
prompts/institutional_diagnostic_chilean_spanish_v0_3.jsonl
prompts/institutional_full_chilean_spanish_v0_3.jsonl
```

## Planned run

Model.

gpt-5.4-mini

Main question.

Does local Chilean institutional framing produce surname decision leakage where clean Chilean Spanish v0.2 did not?