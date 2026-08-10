# Durable accepted-output archive

This directory makes the accepted Phase II scientific output matrix durable in Git rather than relying only on expiring GitHub Actions artifacts.

Each model file contains a deterministic base64 encoding of a gzip-compressed CSV with exactly two columns:

- `prompt_id`
- `parsed_response`

There are exactly 1,032 accepted rows per model and 8,256 rows in total. `parsed_response` is the structured scientific response accepted by the frozen semantic validator. The frozen prompt manifest, profile generator, model panel, and protocol supply the experimental metadata associated with each `prompt_id`.

These compact files intentionally do **not** duplicate transport-level fields such as latency, provider response envelopes, usage accounting, or retry traces. The complete API-level ledgers were verified in the final Actions artifact. Their release-level verifier certificate and artifact provenance are recorded elsewhere under `phase2/results/`.

## Restore and verify

From `phase2/` run:

```bash
python scripts/restore_raw_release.py
```

The script:

1. base64-decodes every archive;
2. decompresses the gzip payload;
3. checks the frozen gzip and CSV SHA256 hashes in `MANIFEST.json`;
4. verifies 1,032 unique prompt IDs per model;
5. verifies each `parsed_response` is valid JSON;
6. writes human-readable CSVs to `results/parsed_release/`;
7. refuses to finish unless the total is exactly 8,256 accepted outputs.

## File naming note

The Claude archive retains the historical filename `claude_sonnet5.jsonl.gz.b64`. Its internal payload is CSV, like the other seven model archives, and `MANIFEST.json` records this explicitly. The filename is retained to avoid rewriting the already archived evidence blob solely for cosmetic consistency.

## Scope

This archive is sufficient to audit and independently reanalyse the accepted scientific responses when joined to the frozen prompt manifest. Exact transport-level reproduction of the final release verifier additionally depends on the full historical API ledger referenced in the release provenance record.
