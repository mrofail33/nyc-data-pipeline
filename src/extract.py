import requests

from src.config import NYC_311_API_URL, RECORD_LIMIT, SOCRATA_APP_TOKEN


FIELDS = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "status",
    "borough",
    "incident_zip",
    "city",
    "resolution_description",
    "latitude",
    "longitude",
]


def extract_311_records():
    """Download recent NYC 311 records from the NYC Open Data API."""
    params = {
        "$select": ", ".join(FIELDS),
        "$limit": RECORD_LIMIT,
        "$order": "created_date DESC",
    }

    headers = {}
    if SOCRATA_APP_TOKEN:
        headers["X-App-Token"] = SOCRATA_APP_TOKEN

    response = requests.get(
        NYC_311_API_URL,
        params=params,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
