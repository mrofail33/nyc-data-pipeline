from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.load import get_connection


CHARTS_DIR = Path("charts")


def save_chart(query, title, filename, x_column, y_column):
    with get_connection() as connection:
        df = pd.read_sql_query(query, connection)

    if df.empty:
        print(f"No data for {title}")
        return

    CHARTS_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.bar(df[x_column].astype(str), df[y_column])
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / filename)
    plt.close()
    print(f"Saved {CHARTS_DIR / filename}")


def main():
    save_chart(
        """
        SELECT borough, COUNT(*) AS complaint_count
        FROM service_requests
        GROUP BY borough
        ORDER BY complaint_count DESC;
        """,
        "Complaints by Borough",
        "complaints_by_borough.png",
        "borough",
        "complaint_count",
    )

    save_chart(
        """
        SELECT complaint_type, COUNT(*) AS complaint_count
        FROM service_requests
        GROUP BY complaint_type
        ORDER BY complaint_count DESC
        LIMIT 10;
        """,
        "Top Complaint Types",
        "top_complaint_types.png",
        "complaint_type",
        "complaint_count",
    )


if __name__ == "__main__":
    main()
