# NYC 311 Data Pipeline

[![CI](https://github.com/mrofail33/nyc-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/mrofail33/nyc-data-pipeline/actions/workflows/ci.yml)

A Python ETL pipeline that retrieves NYC 311 requests, cleans them with pandas, and provides PostgreSQL loading and SQL analysis modules.

## Data flow

NYC Open Data API -> pandas transformation -> PostgreSQL -> SQL analysis and optional charts.

Transformations deduplicate request IDs, reject rows without a request ID or creation date, normalize text/date fields, fill missing text with `Unknown`, and calculate resolution time and creation month.

## Run

```bash
python -m venv .venv
# Activate .venv for your shell.
pip install -r requirements.txt
# Copy .env.example to .env and configure DATABASE_URL.
docker compose up -d
python -m src.pipeline
python -m src.charts
```

SQL queries are in `database/analysis_queries.sql`. The source is [NYC 311 Service Requests](https://data.cityofnewyork.us/resource/erm2-nwe9.json); configure `RECORD_LIMIT` to adjust the download size.

## Verification

```bash
python -m pytest -q
```

Focused transform tests are in `tests/`, and GitHub Actions runs them. Archived evidence in `docs/benchmark-results/nyc_311_pipeline_2026-09-23.json` records 10,000 retrieved and cleaned rows, 3,906 missing text values handled, and a five-second extract/transform run. PostgreSQL was unavailable during that benchmark, so **database loading was not verified**. Do not describe that run as 10,000 rows loaded.

## Limitations

This is a local pipeline. Results describe a point-in-time API response and vary as public data changes. Loading and chart generation require the configured PostgreSQL service.
