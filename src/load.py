from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

from src.config import DATABASE_URL


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_table():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_PATH.read_text())


def load_records(df):
    """Insert cleaned records into PostgreSQL."""
    if df.empty:
        print("No records to load.")
        return 0

    columns = list(df.columns)
    values = [tuple(row) for row in df.where(df.notna(), None).to_numpy()]

    insert_sql = f"""
        INSERT INTO service_requests ({", ".join(columns)})
        VALUES %s
        ON CONFLICT (unique_key) DO UPDATE SET
            created_date = EXCLUDED.created_date,
            closed_date = EXCLUDED.closed_date,
            agency = EXCLUDED.agency,
            agency_name = EXCLUDED.agency_name,
            complaint_type = EXCLUDED.complaint_type,
            descriptor = EXCLUDED.descriptor,
            status = EXCLUDED.status,
            borough = EXCLUDED.borough,
            incident_zip = EXCLUDED.incident_zip,
            city = EXCLUDED.city,
            resolution_description = EXCLUDED.resolution_description,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            resolution_time_hours = EXCLUDED.resolution_time_hours,
            created_month = EXCLUDED.created_month;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            execute_values(cursor, insert_sql, values)

    return len(df)
