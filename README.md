# Student Performance Data Pipeline

A beginner-friendly **Python Data Engineering** project that reads student exam records from a CSV file, validates and cleans the data, transforms it, and loads the results into a SQLite database. It also creates summary reports.

## What this project demonstrates

- **Extract:** read raw CSV data with Python and pandas.
- **Transform:** standardize column names, remove duplicates, handle missing values, validate scores, and calculate total/average scores and grades.
- **Load:** save cleaned records into a SQLite database.
- **Report:** generate CSV summaries by class and grade.
- **Logging:** record pipeline progress and errors.

## Project architecture

```text
student-performance-etl/
├── data/
│   └── students.csv             # Sample input data
├── reports/                     # Generated summary CSV files
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

```text
CSV file
   |
   v
EXTRACT (pandas)
   |
   v
TRANSFORM (clean + validate + calculate)
   |
   v
LOAD (SQLite database)
   |
   v
REPORTS (class and grade summaries)
```

## Requirements

- Python 3.9 or newer
- pip

## Run locally

### 1. Download or clone this repository

```bash
git clone https://github.com/YOUR-USERNAME/student-performance-etl.git
cd student-performance-etl
```

If you downloaded the ZIP, extract it and open a terminal in the extracted folder.

### 2. Create a virtual environment (recommended)

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python main.py
```

You should see a success message. The first run creates:

- `student_performance.db` — SQLite database containing the cleaned student records.
- `reports/class_summary.csv` — average scores grouped by class.
- `reports/grade_summary.csv` — student counts grouped by grade.
- `pipeline.log` — execution log.

The database and generated reports are created locally and are ignored by Git by default. The sample input CSV is included in the repository.

## Sample data

`data/students.csv` contains fictional student records with a few intentional data-quality issues (a duplicate row and a missing score) so you can see the cleaning steps in action. No real student information is used.

## Data rules

1. Column names are converted to lowercase and standardized.
2. Exact duplicate rows are removed.
3. Rows with missing student IDs or class names are removed.
4. Missing subject scores are filled with that subject's median score.
5. Scores outside the range 0–100 are treated as invalid and replaced with the subject median.
6. Total and average scores are calculated.
7. Grades are assigned using the average score:
   - A: 90–100
   - B: 80–89.99
   - C: 70–79.99
   - D: 60–69.99
   - F: below 60

## Inspect the SQLite database

You can open `student_performance.db` using [DB Browser for SQLite](https://sqlitebrowser.org/) or Python:

```python
import sqlite3
import pandas as pd

connection = sqlite3.connect("student_performance.db")
students = pd.read_sql_query("SELECT * FROM student_performance", connection)
print(students.head())
connection.close()
```

## Example SQL queries

```sql
-- Top five students by average score
SELECT student_id, student_name, average_score, grade
FROM student_performance
ORDER BY average_score DESC
LIMIT 5;

-- Average score by class
SELECT class_name, ROUND(AVG(average_score), 2) AS class_average
FROM student_performance
GROUP BY class_name;
```

## Customizing the project

- Add more rows to `data/students.csv`.
- Add another subject by updating the CSV columns and the `SUBJECT_COLUMNS` list in `src/config.py`.
- Change grade boundaries in `src/transform.py`.
- Add new reports in `src/pipeline.py`.

## GitHub upload

### Option A: GitHub website (no Git commands)

1. Sign in at https://github.com/.
2. Click **New repository**.
3. Enter `student-performance-etl` as the repository name.
4. Choose **Public** (or Private if preferred), then click **Create repository**.
5. In the new repository, choose **Add file → Upload files**.
6. Upload the project files and folders from this extracted project directory. Do not upload `.venv`, the database, logs, or generated reports.
7. Click **Commit changes**.

### Option B: Git commands

Create an empty repository on GitHub named `student-performance-etl`, then run these commands from this project folder:

```bash
git init
git add .
git commit -m "Add student performance ETL pipeline"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/student-performance-etl.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If Git asks you to authenticate, follow GitHub's sign-in flow.

## Future improvements

- Add automated tests with `pytest`.
- Add data visualizations.
- Schedule the pipeline to run daily.
- Replace SQLite with PostgreSQL.
- Add a dashboard using Streamlit.

## License

This project is provided for learning and educational use. You may modify it for your own portfolio.
