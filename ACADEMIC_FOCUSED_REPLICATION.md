# Academic focused replication v0.5

The Chilean institutional framing run produced the first suggestive decision leakage signal.

That signal was concentrated in single profile academic selection.

The focused replication tested whether that signal survives a larger run.

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

This could have been a real signal, or it could have been small-sample noise from the prompt generator.

The focused academic run tested that directly.

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

The generator used:

- 10 elite coded surnames
- 10 common baseline surnames
- 20 first names
- 5 academic contexts

Total prompts.

2000

## Run result

Model.

gpt-5.4-mini

Language.

Chilean Spanish

Run health.

| Item | Result |
| --- | ---: |
| Total prompts | 2000 |
| Elite-coded prompts | 1000 |
| Common baseline prompts | 1000 |
| API errors | 0 |
| JSON parse failures | 0 |
| Explanation leakage | 0 |
| Total tokens | 293,618 |

## Main result

The academic focused run did not replicate the institutional academic gap.

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

## Rating distribution

| Group | Rating 6 | Rating 7 |
| --- | ---: | ---: |
| Elite coded | 580 | 420 |
| Common baseline | 582 | 418 |

The difference is two extra 7 ratings for elite-coded surnames across 1000 prompts.

That is not meaningful.

## By academic context

| Context | Elite avg | Common avg | Difference |
| --- | ---: | ---: | ---: |
| Research assistant | 6.105 | 6.090 | +0.015 |
| Research project support | 6.000 | 6.000 | 0.000 |
| Teaching assistant | 7.000 | 7.000 | 0.000 |
| Academic mentoring | 6.995 | 7.000 | -0.005 |
| Short academic internship | 6.000 | 6.000 | 0.000 |

The model mostly responded to the academic context wording.

Some contexts almost always got 6.

Some contexts almost always got 7.

Surname barely moved the rating.

## By surname

Elite-coded surnames ranged from 6.40 to 6.45.

Common baseline surnames also ranged from 6.40 to 6.45.

| Surname | Group | Average |
| --- | --- | ---: |
| Schmidt | Elite | 6.45 |
| Vial | Elite | 6.44 |
| García-Huidobro | Elite | 6.40 |
| Larraín | Elite | 6.40 |
| Soto | Common | 6.45 |
| Flores | Common | 6.43 |
| González | Common | 6.40 |
| Pérez | Common | 6.40 |

There is no stable elite advantage.

## Interpretation

The earlier academic-selection gap did not survive replication.

The institutional v0.3 academic gap should now be treated as a likely small-sample or prompt-context artifact.

This is useful because it keeps the study from overclaiming.

Current status.

- Strong evidence for status knowledge.
- Strong evidence for institution prestige mapping.
- No stable evidence for academic decision leakage in the focused replication.

## Updated interpretation rule

Institution prestige mapping is now the main positive finding.

Academic decision leakage is not supported by the focused replication.

The cleaner claim is:

The model carries a Chilean surname-to-institution prestige map, but this did not translate into stable academic ratings in the focused test.