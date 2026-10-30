import sqlite3

import pandas as pd


def load_data(df, database_path):
    """Load transformed records into a SQLite table."""
    with sqlite3.connect(database_path) as connection:
        df.to_sql(
            "student_performance",
            connection,
            if_exists="replace",
            index=False,
        )


def create_reports(df, reports_dir):
    """Write useful summary CSV files."""
    reports_dir.mkdir(parents=True, exist_ok=True)

    class_summary = (
        df.groupby("class_name", as_index=False)
        .agg(
            student_count=("student_id", "count"),
            average_score=("average_score", "mean"),
        )
    )
    class_summary["average_score"] = class_summary["average_score"].round(2)
    class_summary.to_csv(reports_dir / "class_summary.csv", index=False)

    grade_summary = (
        df.groupby("grade")
        .size()
        .reset_index(name="student_count")
        .sort_values("grade")
    )
    grade_summary.to_csv(reports_dir / "grade_summary.csv", index=False)
