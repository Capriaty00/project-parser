import os
import xml.etree.ElementTree as ET
from utils.logger import get_logger

logger = get_logger(__name__)


def parse_xml(file_path: str) -> dict:
    if not os.path.exists(file_path):
        logger.error(f"Fichier XML introuvable : {file_path}")
        raise FileNotFoundError(file_path)

    logger.info(f"Parsing XML : {file_path}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        records = []
        for element in root:
            record = {child.tag: child.text for child in element}
            records.append(record)

        logger.info(f"{len(records)} éléments parsés depuis le XML")

        return {
            "format": "xml",
            "source": file_path,
            "records": records
        }

    except ET.ParseError as e:
        logger.error(f"XML invalide : {e}")
        raise
