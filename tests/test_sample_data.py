import json
import unittest
from pathlib import Path
from app.io import read_collection

class SampleDataTests(unittest.TestCase):
    def test_sample_is_readable_and_matches_schema_fields(self):
        root = Path(__file__).resolve().parents[1]
        data = read_collection(root / "data" / 'records.json')
        schema = json.loads((root / "schema.json").read_text(encoding="utf-8"))
        rows = data[schema["collection"].removesuffix(".json")] if schema["collection"].removesuffix(".json") in data else next(iter(data.values()))
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)
        self.assertTrue(set(schema["record_fields"]).issubset(rows[0]))
        self.assertTrue(all(isinstance(row, dict) for row in rows))

    def test_loader_rejects_non_object_root(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_collection(path)
