import pandas as pd


def extract_data(csv_path):
    """Read raw student records from a CSV file."""
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Input file was not found: {csv_path}. "
            "Check that data/students.csv exists."
        ) from exc
