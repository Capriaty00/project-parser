from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def _setup_logger(level: str) -> logging.Logger:
    """
    Try to use project_parser.utils.logger.setup_logger if available,
    otherwise fall back to basic logging.
    """
    try:
        from project_parser.utils.logger import setup_logger  # type: ignore

        return setup_logger(level=level)
    except Exception:
        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )
        return logging.getLogger("project_parser")


def _detect_format(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    if ext in {"csv", "json", "xml"}:
        return ext
    raise ValueError(f"Unsupported file extension: .{ext}")


def _load_parser(fmt: str):
    """
    Lazy import to avoid breaking the CLI branch before parsers exist.
    xoxo will implement:
      - project_parser.parsers.csv_parser.CSVParser
      - project_parser.parsers.json_parser.JSONParser
      - project_parser.parsers.xml_parser.XMLParser
    Each must expose .parse(filepath: str) -> List[Dict[str, Any]]
    """
    try:
        if fmt == "csv":
            from project_parser.parsers.csv_parser import CSVParser  # type: ignore

            return CSVParser()
        if fmt == "json":
            from project_parser.parsers.json_parser import JSONParser  # type: ignore

            return JSONParser()
        if fmt == "xml":
            from project_parser.parsers.xml_parser import XMLParser  # type: ignore

            return XMLParser()
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "Parser modules are not available yet. "
            "Wait for xoxo to merge the parsers PR (feat(parsers))."
        ) from e

    raise ValueError(f"Unsupported format: {fmt}")


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="project-parser",
        description="Multi-format parser (CSV/JSON/XML) -> List[Dict[str, Any]] with logs",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input file (csv/json/xml)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "xml"],
        default=None,
        help="Force format (otherwise inferred from file extension)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print output as JSON",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    logger = _setup_logger(args.log_level)

    input_path = Path(args.input)

    if not input_path.exists():
        logger.error("File not found: %s", input_path)
        return 1
    if not input_path.is_file():
        logger.error("Input is not a file: %s", input_path)
        return 1

    try:
        fmt = args.format or _detect_format(input_path)
    except ValueError as e:
        logger.error(str(e))
        return 1

    logger.info("Input: %s", input_path)
    logger.info("Format: %s", fmt)

    try:
        parser = _load_parser(fmt)
        data: List[Dict[str, Any]] = parser.parse(str(input_path))
    except Exception as e:
        logger.exception("Parsing failed: %s", e)
        return 1

    logger.info("Parsed rows: %d", len(data))

    if args.pretty:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(data)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
