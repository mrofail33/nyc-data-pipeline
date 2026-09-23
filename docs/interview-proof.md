# Interview Proof

This project is intentionally a small ETL pipeline. The safest interview claim is:

> I built a Python ETL pipeline that pulls NYC 311 records from a public API, cleans the data with pandas, loads it into PostgreSQL, and supports SQL analysis.

## What the repo now proves

- `src/extract.py` calls the NYC Open Data API.
- `src/transform.py` cleans dates, text fields, duplicates, ZIP codes, coordinates, and resolution time.
- `src/load.py` creates and upserts into PostgreSQL.
- `database/analysis_queries.sql` contains the SQL analysis layer.
- `tests/test_transform.py` proves the most important cleaning logic.
- `.github/workflows/ci.yml` proves the tests can run from a fresh checkout.

## What not to claim yet

- Production data platform.
- Cloud data warehouse.
- Airflow, dbt, Spark, or orchestration.
- Real-time streaming.

## Next simple upgrade

Add a scheduled run with GitHub Actions or Prefect and save a small `sample_output/` folder with row counts and chart screenshots.
