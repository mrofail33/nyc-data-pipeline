from src.extract import extract_311_records
from src.load import create_table, load_records
from src.transform import transform_311_records


def run_pipeline():
    print("Extract: downloading NYC 311 records...")
    raw_records = extract_311_records()
    print(f"Extract: downloaded {len(raw_records)} records.")

    print("Transform: cleaning records with pandas...")
    cleaned_records = transform_311_records(raw_records)
    print(f"Transform: prepared {len(cleaned_records)} clean records.")

    print("Load: creating table if needed...")
    create_table()

    print("Load: inserting records into PostgreSQL...")
    inserted_count = load_records(cleaned_records)
    print(f"Done: loaded {inserted_count} records into PostgreSQL.")


if __name__ == "__main__":
    run_pipeline()
