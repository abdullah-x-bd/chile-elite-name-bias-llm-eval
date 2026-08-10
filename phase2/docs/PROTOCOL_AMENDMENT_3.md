# Protocol Amendment 3, outcome-blind execution repair

Date: 2026-08-10

Status: specified after Phase II collection began but before any scientific response value was inspected.

Under Amendment 2, the Claude Sonnet 5 cell successfully produced and locally appended 125 scientific responses. On the next request, Anthropic returned a truncated structured response that ended mid-JSON under the frozen 80-token output budget. The job terminated before uploading its local JSONL artifact. The 125 response values were therefore not retrieved or inspected. The Actions log exposed only progress counts, cumulative cost, and the JSON parsing error.

Observed operational facts before this amendment:

- 125 Claude scientific requests completed before failure;
- cumulative Claude cost reported at the last progress checkpoint was approximately $0.1674;
- the failing response was syntactically incomplete JSON;
- no Claude scientific response values were inspected or used in analysis;
- no other model's scientific results were inspected before this amendment was specified.

## Amendment

For the complete Claude Sonnet 5 primary cell only, change `reasoning` from `low` to `omit` while preserving:

- model `anthropic/claude-sonnet-5`;
- canonical model `anthropic/claude-sonnet-5-20260630`;
- provider `anthropic`;
- 80-token output cap;
- all 1,032 scientific prompts and hashes;
- provider-facing Anthropic schema compatibility adapter from Amendment 1;
- post-response semantic bounds and validation;
- all hypotheses, estimands, analysis rules, and exclusions.

The complete Claude cell is rerun from the beginning under Amendment 3 because the partial local artifact from Amendment 2 was not uploaded. The unrecovered Amendment 2 Claude calls are excluded from the scientific dataset but included in the project-level expenditure audit.

## Other model cells

No successfully completed model cell is rerun. Their exact artifacts are recovered from the original primary GitHub Actions run and combined with the Amendment 3 Claude artifact before release verification.

## Scientific interpretation

Amendment 3 is an execution-compatibility repair, not an outcome-driven analytical change. It was motivated only by a truncated JSON response and was specified without inspecting any surname-association or decision-leakage result.
