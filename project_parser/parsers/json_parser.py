import json
import os
from typing import Any, Dict, List

from project_parser.utils.logger import setup_logger

logger = setup_logger()


def parse_json(file_path: str) -> Dict[str, Any]:
    """
    Parse a JSON file and return a dict with metadata + records.
    Kept for backward compatibility.
    """
    if not os.path.exists(file_path):
        logger.error(f"Fichier JSON introuvable : {file_path}")
        raise FileNotFoundError(file_path)

    logger.info(f"Parsing JSON : {file_path}")

    try:
        with open(file_path, encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)

        if isinstance(data, dict):
            records = [data]
        elif isinstance(data, list):
            records = data
        else:
            logger.warning("Structure JSON inattendue, records vide")
            records = []

        logger.info(f"{len(records)} enregistrements parsés depuis le JSON")

        return {"format": "json", "source": file_path, "records": records}

    except json.JSONDecodeError as e:
        logger.error(f"JSON invalide : {e}")
        raise


class JSONParser:
    """
    Parser compatible avec la CLI (main.py).
    Doit exposer: parse(filepath) -> List[Dict[str, Any]]
    """

    def parse(self, filepath: str) -> List[Dict[str, Any]]:
        payload = parse_json(filepath)
        records = payload.get("records", [])
        if not isinstance(records, list):
            raise ValueError("JSON records must be a list of dicts")
        return records
