# data_loader.py
import sys
from pathlib import Path
import pandas as pd
from utils.logger import logging
from utils.custom_exception import CustomException

class AnimeDataLoader:
    """
    Loads a raw CSV, validates required columns, builds a `combined_info` text field,
    and writes a processed CSV with one column: combined_info.
    """
    def __init__(self, original_csv: str, processed_csv: str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self) -> str:
        # 1) Basic path checks
        try:
            if not Path(self.original_csv).exists():
                raise FileNotFoundError(f"Input CSV not found: {self.original_csv}")
        except Exception as e:
            raise CustomException("Path validation failed", sys) from e

        # 2) Validate header/required columns fast
        try:
            header_df = pd.read_csv(self.original_csv, nrows=1, encoding="utf-8", on_bad_lines="skip")
            required = {"Name", "Genres", "synopsis"}
            missing = required - set(header_df.columns)
            if missing:
                raise ValueError(f"Missing required columns: {sorted(missing)}")
        except Exception as e:
            raise CustomException("CSV header validation failed", sys) from e

        # 3) Load full file
        try:
            df = pd.read_csv(self.original_csv, encoding="utf-8", on_bad_lines="skip")
        except Exception as e:
            raise CustomException("Failed to read full CSV", sys) from e

        # 4) Clean & build combined_info
        try:
            # Only drop rows missing required fields
            df = df.dropna(subset=["Name", "Genres", "synopsis"])

            # Normalize to strings and strip
            df["Name"] = df["Name"].astype(str).str.strip()
            df["Genres"] = df["Genres"].astype(str).str.strip()
            df["synopsis"] = df["synopsis"].astype(str).str.strip()

            df["combined_info"] = (
                "Title: " + df["Name"] +
                "Overview: " + df["synopsis"] +
                " Genres: " + df["Genres"]
            )
        except Exception as e:
            raise CustomException("Failed while building combined_info", sys) from e

        # 5) Save processed CSV (only the combined column)
        try:
            df[["combined_info"]].to_csv(self.processed_csv, index=False, encoding="utf-8")
            logging.info(f"Processed {len(df)} rows -> {self.processed_csv}")
            return str(self.processed_csv)
        except Exception as e:
            raise CustomException("Failed to write processed CSV", sys) from e
