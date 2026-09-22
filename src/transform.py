import pandas as pd

from src.extract import FIELDS


TEXT_COLUMNS = [
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "status",
    "borough",
    "incident_zip",
    "city",
    "resolution_description",
]


def _clean_text(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Unknown"
    return str(value).strip()


def transform_311_records(records):
    """Clean and organize raw NYC 311 records with pandas."""
    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(columns=FIELDS + ["resolution_time_hours", "created_month"])

    df = df.reindex(columns=FIELDS)

    df = df.drop_duplicates(subset=["unique_key"])
    df = df.dropna(subset=["unique_key", "created_date"])

    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
    df = df.dropna(subset=["created_date"])

    for column in TEXT_COLUMNS:
        df[column] = df[column].apply(_clean_text)

    df["agency"] = df["agency"].str.upper()
    df["borough"] = df["borough"].str.upper()
    df["status"] = df["status"].str.upper()
    df["complaint_type"] = df["complaint_type"].str.title()
    df["descriptor"] = df["descriptor"].str.title()
    df["city"] = df["city"].str.title()
    df["incident_zip"] = df["incident_zip"].str[:5]

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    resolution_time = df["closed_date"] - df["created_date"]
    df["resolution_time_hours"] = resolution_time.dt.total_seconds() / 3600
    df.loc[df["resolution_time_hours"] < 0, "resolution_time_hours"] = None

    df["created_month"] = df["created_date"].dt.to_period("M").astype(str)

    return df[
        [
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
            "resolution_time_hours",
            "created_month",
        ]
    ]
