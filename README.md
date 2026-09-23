# NYC Data Pipeline

A simple, interview-friendly ETL project that downloads NYC 311 service request data, cleans it with pandas, and loads it into PostgreSQL for SQL analysis.

The project intentionally keeps the code straightforward:

```text
Extract  ->  Transform  ->  Load
NYC API      pandas          PostgreSQL
```

## Project Structure

```text
nyc-data-pipeline/
├── database/
│   ├── schema.sql
│   └── analysis_queries.sql
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── pipeline.py
│   └── charts.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Dataset

This project uses NYC Open Data's 311 Service Requests dataset:

- Dataset: `311 Service Requests from 2020 to Present`
- Dataset ID: `erm2-nwe9`
- API endpoint: `https://data.cityofnewyork.us/resource/erm2-nwe9.json`
- Source page: `https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9`

The pipeline downloads the latest records from the API, ordered by `created_date`.

## Chosen Fields

The project keeps a small set of useful columns:

| Field | Meaning |
| --- | --- |
| `unique_key` | Unique 311 service request ID |
| `created_date` | When the complaint was created |
| `closed_date` | When the complaint was closed |
| `agency` | Short agency code |
| `agency_name` | Full agency name |
| `complaint_type` | Main type of complaint |
| `descriptor` | More specific complaint description |
| `status` | Current complaint status |
| `borough` | NYC borough |
| `incident_zip` | ZIP code |
| `city` | City name |
| `resolution_description` | Resolution text from 311 |
| `latitude` | Latitude |
| `longitude` | Longitude |
| `resolution_time_hours` | Hours between created and closed date |
| `created_month` | Month extracted from created date |

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your environment file

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 4. Start PostgreSQL

The easiest option is Docker:

```bash
docker compose up -d
```

This starts a local PostgreSQL database using the connection string already shown in `.env.example`:

```text
postgresql://postgres:postgres@localhost:5432/nyc_data_pipeline
```

If you already have PostgreSQL installed, create a database named `nyc_data_pipeline` and update `DATABASE_URL` in `.env`.

## Run the ETL Pipeline

```bash
python -m src.pipeline
```

What happens:

1. **Extract**: downloads recent 311 records from the NYC Open Data API.
2. **Transform**: cleans the data with pandas.
3. **Load**: creates the PostgreSQL table and inserts the cleaned records.

You can change how many records are downloaded by editing `RECORD_LIMIT` in `.env`.

## Run SQL Analysis

After running the pipeline, open PostgreSQL and run:

```bash
psql postgresql://postgres:postgres@localhost:5432/nyc_data_pipeline
```

Then run the queries from:

```text
database/analysis_queries.sql
```

The included analysis queries answer:

- Complaints by borough
- Most common complaint types
- Complaints by month
- Average resolution time
- Busiest complaint periods by hour of day

## Optional Charts

After loading data, create a few simple charts:

```bash
python -m src.charts
```

Charts are saved in the `charts/` folder.

## What the Pipeline Cleans

The transform step does a few practical cleaning tasks:

- Removes duplicate records using `unique_key`
- Drops records without a `unique_key` or `created_date`
- Converts `created_date` and `closed_date` into real datetime values
- Fills missing text fields with `Unknown`
- Standardizes borough and status values
- Converts latitude and longitude into numbers
- Creates `resolution_time_hours`
- Creates `created_month`
- Selects only useful columns for analysis

## Measured Pipeline Run

Benchmark completed on 2026-09-23 with `RECORD_LIMIT=10000` using the live NYC Open Data API. Raw evidence is saved in `docs/benchmark-results/nyc_311_pipeline_2026-09-23.json`.

| Raw records downloaded | Duplicates removed | Rows missing key/date | Missing text values handled | Final rows ready to load | Final rows loaded | Runtime |
| ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 10,000 | 0 | 0 | 3,906 | 10,000 | Not loaded: PostgreSQL unavailable | 5.00 sec |

The extract and transform stages completed successfully. The load stage was blocked because no PostgreSQL server was listening on `localhost:5432`, so this run does not claim rows loaded into PostgreSQL.

## Interview Explanation

> I built an ETL pipeline in Python that extracts NYC 311 service request records from NYC Open Data, transforms the data with pandas by cleaning dates, missing values, duplicates, and text fields, and loads the cleaned data into PostgreSQL for SQL analysis.

If someone asks, "What is ETL?"

> ETL means Extract, Transform, Load. In this project, I extract records from the NYC API, transform them by cleaning and organizing the data with pandas, and load the final dataset into PostgreSQL.

## Why This Project Is Useful

This project shows that you can:

- Work with a real public API
- Clean messy real-world data
- Store data in a relational database
- Write SQL queries for analysis
- Explain a complete data pipeline in simple terms

## Interview Proof

This is a local ETL project, not a production data platform. The repo now includes:

- focused transform tests in `tests/`
- a GitHub Actions CI workflow in `.github/workflows/ci.yml`
- an interview-safe explanation in `docs/interview-proof.md`
- operations proof notes in `docs/operations-proof.md`

Safe resume wording:

> Built a Python ETL pipeline that extracts NYC 311 data from a public API, cleans and normalizes it with pandas, loads it into PostgreSQL, and supports SQL analysis.

Resume-ready quantified bullet:

- Processed 10,000 live NYC 311 records in 5.00 seconds through extract and transform, handling 3,906 missing text values and preparing 10,000 cleaned rows for loading; PostgreSQL load verification was blocked because the local database service was unavailable.
