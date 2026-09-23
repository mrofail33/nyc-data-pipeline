# Operations Proof

Safe interview claim:

> I built the ETL as a repeatable pipeline with config, tests, Dockerized PostgreSQL, and a clear path to scheduling.

## Current proof

- `docker-compose.yml` starts PostgreSQL locally.
- `.env.example` documents configurable database and record-limit settings.
- `.github/workflows/ci.yml` runs transform tests on push and pull request.
- `src/pipeline.py` is the single command entry point for extract, transform, and load.
- `database/analysis_queries.sql` documents the analysis layer after loading.

## What not to claim yet

- Do not claim Airflow, dbt, Spark, or a cloud warehouse.
- Do not claim production scheduling is already deployed.
- Do not claim streaming data ingestion.

## Simple next upgrade

Add a scheduled GitHub Actions workflow that runs the pipeline on a small record limit and stores a row-count summary as a workflow artifact.
