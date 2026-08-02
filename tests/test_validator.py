from __future__ import annotations

import sys
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def test_canonical_data_is_valid(self) -> None:
        self.assertEqual([], validate.validate())

    def test_no_entity_is_silently_quarantined(self) -> None:
        entities = validate.load_json("data/entities.v1.json")["entities"]
        quarantined = [entity for entity in entities if entity["disposition"] == "quarantined"]
        self.assertGreaterEqual(len(quarantined), 4)
        self.assertTrue(all(entity.get("quarantineReason") for entity in quarantined))

    def test_each_destructive_fixture_fails_at_its_json_pointer(self) -> None:
        for path in sorted((ROOT / "tests/fixtures/invalid").glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            errors = validate.validate_fixture_document(document)
            self.assertTrue(any(error.startswith(document["expectedPointer"]) for error in errors), f"{path}: {errors}")

    def test_duplicate_and_cyclic_aliases_are_rejected(self) -> None:
        duplicate = validate.validate_alias_records([{"alias": "x", "target": "entity"}, {"alias": "x", "target": "entity"}], {"entity"})
        self.assertTrue(any("duplicate alias" in error for error in duplicate))
        cyclic = validate.validate_alias_records([{"alias": "x", "target": "y"}, {"alias": "y", "target": "x"}], {"entity"})
        self.assertTrue(any("cyclic alias" in error for error in cyclic))


if __name__ == "__main__":
    unittest.main()
