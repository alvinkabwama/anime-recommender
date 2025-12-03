# build_pipeline.py

import sys
from pathlib import Path

from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

# Resolve project root = one level up from this file (pipeline/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_CSV_PATH = PROJECT_ROOT / "data" / "anime_with_synopsis.csv"
PROCESSED_CSV_PATH = PROJECT_ROOT / "data" / "anime_updated.csv"


def run_build_pipeline(
    raw_csv: Path = RAW_CSV_PATH,
    processed_csv: Path = PROCESSED_CSV_PATH,
) -> None:
    try:
        logger.info("Starting anime build pipeline.")
        logger.info("Raw CSV: %s", raw_csv)
        logger.info("Processed CSV: %s", processed_csv)

        processed_csv.parent.mkdir(parents=True, exist_ok=True)

        loader = AnimeDataLoader(
            original_csv=str(raw_csv),
            processed_csv=str(processed_csv),
        )
        processed_csv_path = loader.load_and_process()
        logger.info("Data loaded and processed successfully: %s", processed_csv_path)

        vector_store_builder = VectorStoreBuilder(csv_path=processed_csv_path)
        vector_store_builder.build_and_save_vectorstore()
        logger.info("Vector store built and saved successfully.")

        logger.info("Anime build pipeline completed successfully.")

    except Exception as e:
        logger.error("An error occurred in the build pipeline.", exc_info=True)
        raise CustomException("Build pipeline failed", sys) from e


def main() -> None:
    run_build_pipeline()


if __name__ == "__main__":
    main()
