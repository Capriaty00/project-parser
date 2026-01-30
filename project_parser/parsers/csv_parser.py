import csv
import os
from typing import Any, Dict, List

from project_parser.utils.logger import setup_logger

logger = setup_logger()


def parse_csv(file_path: str) -> Dict[str, Any]:
    """
    Parse a CSV file and return a dict with metadata + records.
    Kept for backward compatibility.
    """
    if not os.path.exists(file_path):
        logger.error(f"Fichier CSV introuvable : {file_path}")
        raise FileNotFoundError(file_path)

    logger.info(f"Parsing CSV : {file_path}")

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            records = list(reader)

        logger.info(f"{len(records)} lignes parsées depuis le CSV")

        return {"format": "csv", "source": file_path, "records": records}

    except Exception as e:
        logger.error(f"Erreur parsing CSV : {e}")
        raise


class CSVParser:
    """
    Parser compatible avec la CLI (main.py).
    Doit exposer: parse(filepath) -> List[Dict[str, Any]]
    """

    def parse(self, filepath: str) -> List[Dict[str, Any]]:
        payload = parse_csv(filepath)
        records = payload.get("records", [])
        if not isinstance(records, list):
            raise ValueError("CSV records must be a list of dicts")
        return records
