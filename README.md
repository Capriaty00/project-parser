
# Project Parser

A command-line tool that reads CSV, JSON and XML files and returns their contents
in a single, format-independent Python structure.

Built with the Python standard library only. No external dependencies.

---

## Overview

Data files rarely arrive in a single format. Project Parser reads three common
formats and normalises them into one shared output structure, so that any
downstream component can process the data without knowing where it came from.

The tool is designed to be called either from the command line or as a library
from another Python program.

---

## Requirements

- Python 3.8 or later
- No third-party packages required

---

## Installation

Clone the repository and run the tool as a module from the project root:

```bash
git clone <repository-url>
cd project-parser
```

No installation step is needed.

---

## Usage

### Basic command

```bash
python -m project_parser.main --input examples/test.csv
```

### Options

| Option | Required | Description |
|---|---|---|
| `--input` | Yes | Path to the file to parse |
| `--format` | No | Force a format (`csv`, `json`, `xml`). Inferred from the file extension when omitted |
| `--log-level` | No | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`. Defaults to `INFO` |
| `--pretty` | No | Print the output as indented JSON instead of a raw Python structure |

### Examples

Parse a JSON file with readable output:

```bash
python -m project_parser.main --input examples/test.json --pretty
```

Parse a file whose extension does not match its content:

```bash
python -m project_parser.main --input data/export.txt --format csv
```

Run quietly, reporting errors only:

```bash
python -m project_parser.main --input examples/test.xml --log-level ERROR
```

### Exit codes

| Code | Meaning |
|---|---|
| `0` | The file was parsed successfully |
| `1` | The file was missing, unreadable, malformed, or in an unsupported format |

---

## Output structure

Every parser returns the same type:

```python
List[Dict[str, Any]]
```

Each dictionary represents one record. Keys are field names, values are field
contents. This structure was chosen because it is native to Python, maps
naturally onto all three input formats, and can be consumed directly by a
database loader, an export routine, or an analysis script.

Note on typing: CSV and XML carry no type information, so their values are
returned as strings. JSON preserves the native types found in the source file.
Downstream components should cast values explicitly when needed.

---

## Architecture

```
project_parser/
├── main.py              # CLI: arguments, format detection, orchestration
├── parsers/
│   ├── csv_parser.py    # CSVParser
│   ├── json_parser.py   # JSONParser
│   └── xml_parser.py    # XMLParser
└── utils/
    └── logger.py        # Shared logging service
```

The design follows three layers with a one-way dependency: the CLI calls the
parsers, and no parser imports the CLI. Parsers are loaded lazily inside
`_load_parser`, which means the CLI holds no compile-time reference to any
specific parser.

### Interface contract

Every parser exposes the same method:

```python
def parse(self, filepath: str) -> List[Dict[str, Any]]
```

Because the signature is identical across all three, the CLI treats them
interchangeably and never needs to know which format it is handling.

---

## Using Project Parser as a library

```python
from project_parser.parsers.csv_parser import CSVParser

records = CSVParser().parse("data/users.csv")

for record in records:
    print(record["name"])
```

---

## Format-specific behaviour

### CSV

The first row is read as the header and supplies the dictionary keys. Files are
read as UTF-8. A row with fewer fields than the header yields `None` for the
missing keys.

### JSON

A top-level array is returned as is. A top-level object is wrapped in a
single-element list, so that the return type stays consistent. Any other
top-level type returns an empty list and logs a warning.

### XML

Each direct child of the root element is treated as one record. The child tags
of that element supply the dictionary keys and their text content supplies the
values. XML attributes are not read in the current version.

---

## Error handling

Parsers follow one rule: log, then raise.

No parser silently swallows an error, and no parser terminates the program on
its own. The caller decides what to do with the exception, which keeps the
parsers reusable in contexts where a failure should not stop execution, such as
a batch job processing many files.

Three logging levels are used. `INFO` traces normal execution, including the
file being read and the number of records produced. `WARNING` reports an
unusual but non-blocking situation, such as an unexpected JSON structure.
`ERROR` reports a blocking failure and always precedes a raised exception.

| Situation | Behaviour |
|---|---|
| File not found | `FileNotFoundError` |
| Malformed JSON | `json.JSONDecodeError` |
| Malformed XML | `xml.etree.ElementTree.ParseError` |
| Unsupported extension | `ValueError` |
| Unexpected JSON root type | Empty list, logged as a warning |

---

## Testing

Run the full suite from the project root:

```bash
python -m unittest discover -s tests -t . -v
```

The suite covers nominal cases, edge cases (empty files, header-only files,
incomplete rows, empty tags, separators inside quoted values, accented
characters) and error cases for all three formats. Two additional tests check
that all three parsers honour the shared interface contract and that the same
dataset expressed in three formats produces an identical output.

Test files are generated in a temporary directory and removed after each case,
so the suite runs anywhere without depending on versioned fixtures.

---

## Adding a new format

1. Create a module in `parsers/` implementing the `parse` contract.
2. Add the format to the choices in `main.py` and to `_load_parser`.
3. Add the matching test cases.

No existing parser needs to be modified.

---

## Known limitations

- The interface contract is a team convention, not an enforced abstraction.
  A base class would make it fail at import time rather than at runtime.
- XML attributes are ignored.
- CSV and XML values are not cast to their apparent types.
- Files are loaded fully into memory, which caps the volume that can be
  processed. Streaming would be required for large files.
- No static analysis tooling is configured yet.

---

## Project context

Developed as a team assignment during the third year of the Ynov Bachelor
programme, covering Python packaging, logging, heterogeneous data parsing and
collaborative work with Git.
