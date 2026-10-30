import logging

from src.config import DATA_FILE, DATABASE_FILE, LOG_FILE, REPORTS_DIR
from src.extract import extract_data
from src.load import create_reports, load_data
from src.transform import transform_data


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def run_pipeline():
    """Run the complete Extract -> Transform -> Load workflow."""
    configure_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Pipeline started")
        raw_df = extract_data(DATA_FILE)
        logger.info("Extracted %s raw rows", len(raw_df))

        clean_df = transform_data(raw_df)
        logger.info("Transformed data into %s clean rows", len(clean_df))

        load_data(clean_df, DATABASE_FILE)
        logger.info("Loaded records into %s", DATABASE_FILE)

        create_reports(clean_df, REPORTS_DIR)
        logger.info("Summary reports saved in %s", REPORTS_DIR)
        logger.info("Pipeline completed successfully")

        print("\nPipeline completed successfully!")
        print(f"Clean student records: {len(clean_df)}")
        print(f"SQLite database: {DATABASE_FILE.name}")
        print(f"Reports folder: {REPORTS_DIR}")
    except Exception:
        logger.exception("Pipeline failed")
        raise
