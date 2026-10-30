import pandas as pd

from src.config import SUBJECT_COLUMNS


REQUIRED_COLUMNS = [
    "student_id",
    "student_name",
    "class_name",
    *SUBJECT_COLUMNS,
]


def assign_grade(average):
    """Convert an average score into a letter grade."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def transform_data(raw_df):
    """Clean student records and create calculated columns."""
    df = raw_df.copy()

    # Standardize headers, for example "Math Score" -> "math_score".
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(
            "The input CSV is missing required columns: "
            + ", ".join(missing_columns)
        )

    # Remove exact duplicate records.
    df = df.drop_duplicates()

    # Clean text fields.
    for column in ["student_id", "student_name", "class_name"]:
        df[column] = df[column].astype("string").str.strip()

    # Rows without an ID, name, or class cannot be used reliably.
    df = df.dropna(subset=["student_id", "student_name", "class_name"])
    df = df[
        (df["student_id"] != "")
        & (df["student_name"] != "")
        & (df["class_name"] != "")
    ].copy()

    if df.empty:
        raise ValueError("No valid student records remain after cleaning.")

    # Convert scores to numbers. Non-numeric values become missing.
    for column in SUBJECT_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        df.loc[~df[column].between(0, 100), column] = pd.NA

        median_score = df[column].median()
        if pd.isna(median_score):
            median_score = 0
        df[column] = df[column].fillna(median_score).round(2)

    df["total_score"] = df[SUBJECT_COLUMNS].sum(axis=1).round(2)
    df["average_score"] = (df["total_score"] / len(SUBJECT_COLUMNS)).round(2)
    df["grade"] = df["average_score"].apply(assign_grade)

    # Keep IDs as text so values such as "001" remain unchanged.
    return df.reset_index(drop=True)
