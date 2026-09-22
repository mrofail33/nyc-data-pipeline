import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/nyc_data_pipeline",
)

NYC_311_API_URL = os.getenv(
    "NYC_311_API_URL",
    "https://data.cityofnewyork.us/resource/erm2-nwe9.json",
)

RECORD_LIMIT = int(os.getenv("RECORD_LIMIT", "1000"))
SOCRATA_APP_TOKEN = os.getenv("SOCRATA_APP_TOKEN", "")
