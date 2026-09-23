import pandas as pd

from src.transform import transform_311_records


def test_transform_cleans_and_derives_fields():
    records = [
        {
            "unique_key": "1",
            "created_date": "2026-09-20T10:00:00.000",
            "closed_date": "2026-09-20T14:30:00.000",
            "agency": " nypd ",
            "agency_name": "New York City Police Department",
            "complaint_type": "noise - residential",
            "descriptor": "loud music",
            "status": "closed",
            "borough": "brooklyn",
            "incident_zip": "11201-1234",
            "city": "brooklyn",
            "resolution_description": "",
            "latitude": "40.69",
            "longitude": "-73.99",
        },
        {
            "unique_key": "1",
            "created_date": "2026-09-20T10:00:00.000",
        },
    ]

    cleaned = transform_311_records(records)

    assert len(cleaned) == 1
    row = cleaned.iloc[0]
    assert row["agency"] == "NYPD"
    assert row["borough"] == "BROOKLYN"
    assert row["incident_zip"] == "11201"
    assert row["resolution_description"] == "Unknown"
    assert row["created_month"] == "2026-09"
    assert row["resolution_time_hours"] == 4.5


def test_transform_handles_empty_input():
    cleaned = transform_311_records([])

    assert isinstance(cleaned, pd.DataFrame)
    assert cleaned.empty
    assert "resolution_time_hours" in cleaned.columns
