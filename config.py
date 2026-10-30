from pathlib import Path

# Project root is the parent directory of this src folder.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "students.csv"
DATABASE_FILE = BASE_DIR / "student_performance.db"
REPORTS_DIR = BASE_DIR / "reports"
LOG_FILE = BASE_DIR / "pipeline.log"

SUBJECT_COLUMNS = ["math_score", "science_score", "english_score"]
