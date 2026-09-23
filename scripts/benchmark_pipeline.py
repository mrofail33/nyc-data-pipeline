from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("RECORD_LIMIT", "10000")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.extract import extract_311_records
from src.load import create_table, load_records
from src.transform import TEXT_COLUMNS, transform_311_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Run and measure the NYC 311 ETL pipeline.")
    parser.add_argument("--output", default="docs/benchmark-results/nyc_311_pipeline_2026-09-23.json")
    args = parser.parse_args()

    started = time.perf_counter()
    raw_started = time.perf_counter()
    raw_records = extract_311_records()
    extract_seconds = time.perf_counter() - raw_started

    raw_unique_keys = [record.get("unique_key") for record in raw_records]
    duplicates_removed = len(raw_unique_keys) - len(set(raw_unique_keys))
    missing_unique_or_created = sum(
        1 for record in raw_records if not record.get("unique_key") or not record.get("created_date")
    )
    missing_text_values = sum(
        1
        for record in raw_records
        for column in TEXT_COLUMNS
        if record.get(column) in (None, "")
    )

    transform_started = time.perf_counter()
    cleaned_records = transform_311_records(raw_records)
    transform_seconds = time.perf_counter() - transform_started

    load_started = time.perf_counter()
    load_error = None
    loaded_rows = None
    try:
        create_table()
        loaded_rows = load_records(cleaned_records)
    except Exception as exc:
        load_error = f"{type(exc).__name__}: {exc}"
    load_seconds = time.perf_counter() - load_started

    summary = {
        "benchmark_date": "2026-09-23",
        "requested_record_limit": int(os.environ.get("RECORD_LIMIT", "10000")),
        "raw_records_downloaded": len(raw_records),
        "duplicates_removed": duplicates_removed,
        "rows_missing_unique_key_or_created_date": missing_unique_or_created,
        "missing_text_values_handled": missing_text_values,
        "final_rows_ready_to_load": int(len(cleaned_records)),
        "final_rows_loaded": int(loaded_rows) if loaded_rows is not None else None,
        "load_status": "loaded" if loaded_rows is not None else "blocked",
        "load_error": load_error,
        "extract_seconds": extract_seconds,
        "transform_seconds": transform_seconds,
        "load_seconds": load_seconds,
        "total_runtime_seconds": time.perf_counter() - started,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
