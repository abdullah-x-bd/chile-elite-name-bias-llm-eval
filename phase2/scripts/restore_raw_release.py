from __future__ import annotations

import base64
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "results" / "raw_release"
OUT = ROOT / "results" / "parsed_release"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    manifest = json.loads((ARCHIVE / "MANIFEST.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    seen_global: set[tuple[str, str]] = set()

    for model, spec in manifest["models"].items():
        encoded = "".join((ARCHIVE / spec["file"]).read_text(encoding="utf-8").split())
        gz = base64.b64decode(encoded, validate=True)
        if sha256(gz) != spec["gzip_sha256"]:
            raise RuntimeError(f"gzip hash mismatch for {model}")
        raw = gzip.decompress(gz)
        if sha256(raw) != spec["csv_sha256"]:
            raise RuntimeError(f"CSV hash mismatch for {model}")

        text = raw.decode("utf-8")
        rows = list(csv.DictReader(text.splitlines()))
        if len(rows) != spec["rows"]:
            raise RuntimeError(f"row-count mismatch for {model}: {len(rows)} != {spec['rows']}")
        if set(rows[0]) != {"prompt_id", "parsed_response"}:
            raise RuntimeError(f"unexpected columns for {model}")
        ids = [row["prompt_id"] for row in rows]
        if len(ids) != len(set(ids)):
            raise RuntimeError(f"duplicate prompt_id in {model}")
        for row in rows:
            json.loads(row["parsed_response"])
            key = (model, row["prompt_id"])
            if key in seen_global:
                raise RuntimeError(f"duplicate model/prompt pair: {key}")
            seen_global.add(key)

        (OUT / f"{model}.csv").write_bytes(raw)
        total += len(rows)
        print(f"RESTORED {model}: {len(rows)} rows")

    if total != manifest["total_rows"]:
        raise RuntimeError(f"release total mismatch: {total} != {manifest['total_rows']}")
    print(f"RAW RELEASE RESTORE: PASS ({total} accepted outputs)")


if __name__ == "__main__":
    main()
