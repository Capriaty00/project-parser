import unittest
from pathlib import Path


class TestParsers(unittest.TestCase):
    def test_csv_parser(self):
        from project_parser.parsers.csv_parser import CSVParser

        data = CSVParser().parse(str(Path("examples") / "test.csv"))
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIsInstance(data[0], dict)

    def test_json_parser(self):
        from project_parser.parsers.json_parser import JSONParser

        data = JSONParser().parse(str(Path("examples") / "test.json"))
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIsInstance(data[0], dict)

    def test_xml_parser(self):
        from project_parser.parsers.xml_parser import XMLParser

        data = XMLParser().parse(str(Path("examples") / "test.xml"))
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIsInstance(data[0], dict)


if __name__ == "__main__":
    unittest.main()
