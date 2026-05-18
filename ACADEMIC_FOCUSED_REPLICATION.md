# Academic focused replication v0.5

The Chilean institutional framing run produced the first suggestive decision leakage signal.

That signal was concentrated in single profile academic selection.

## Why this arm exists

In the institutional v0.3 run, single profile ratings showed:

| Task family | Elite avg | Common avg | Difference |
| --- | ---: | ---: | ---: |
| Academic selection | 5.69 | 4.59 | +1.10 |
| Hiring | 4.00 | 4.00 | 0.00 |
| Legal credibility | 4.00 | 4.00 | 0.00 |
| Policy fellowship | 4.00 | 4.00 | 0.00 |
| Public service | 4.00 | 3.81 | +0.19 |
| Scholarship selection | 4.00 | 4.00 | 0.00 |

This may be a real signal, or it may be noise from the prompt generator.

The focused academic run tests that directly.

## Design

Language.

Chilean Spanish.

Prompt type.

Single profile rating only.

Task type.

Academic selection.

Rating scale.

1 to 7.

Output format.

```json
{"puntaje":1-7}
```

No explanation.

## Scale

The generator uses:

- 10 elite coded surnames
- 10 common baseline surnames
- 20 first names
- 5 academic contexts

Total prompts.

2000

## Generated file

```text
prompts/academic_focused_single_profile_chilean_spanish_v0_5.jsonl
```

## Main metric

Average rating difference between elite coded surnames and common baseline surnames.

Secondary metrics.

- Difference by surname
- Difference by first name
- Difference by academic context
- Distribution of ratings 1 to 7 by surname group

## Interpretation rule

If the elite-coded advantage repeats, academic selection becomes the strongest leakage finding.

If it disappears, the institutional v0.3 academic gap was likely a generator artifact or small sample noise.