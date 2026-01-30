import json
import os
from utils.logger import get_logger

logger = get_logger(__name__)


def parse_json(file_path: str) -> dict:
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

        return {
            "format": "json",
            "source": file_path,
            "records": records
        }

    except json.JSONDecodeError as e:
        logger.error(f"JSON invalide : {e}")
        raise
