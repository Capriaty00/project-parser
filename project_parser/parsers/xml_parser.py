import os
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

from project_parser.utils.logger import setup_logger

logger = setup_logger()


def parse_xml(file_path: str) -> Dict[str, Any]:
    """
    Parse an XML file and return a dict with metadata + records.
    Kept for backward compatibility.
    Expected XML format:
      <root>
        <row><id>1</id><name>Alice</name></row>
        ...
      </root>
    """
    if not os.path.exists(file_path):
        logger.error(f"Fichier XML introuvable : {file_path}")
        raise FileNotFoundError(file_path)

    logger.info(f"Parsing XML : {file_path}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        records: List[Dict[str, Any]] = []
        for element in root:
            record = {child.tag: child.text for child in element}
            records.append(record)

        logger.info(f"{len(records)} éléments parsés depuis le XML")

        return {"format": "xml", "source": file_path, "records": records}

    except ET.ParseError as e:
        logger.error(f"XML invalide : {e}")
        raise


class XMLParser:
    """
    Parser compatible avec la CLI (main.py).
    Doit exposer: parse(filepath) -> List[Dict[str, Any]]
    """

    def parse(self, filepath: str) -> List[Dict[str, Any]]:
        payload = parse_xml(filepath)
        records = payload.get("records", [])
        if not isinstance(records, list):
            raise ValueError("XML records must be a list of dicts")
        return records
