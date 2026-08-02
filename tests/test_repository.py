import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frameworks = json.loads((DATA / "frameworks.json").read_text(encoding="utf-8"))
        cls.concepts = json.loads((DATA / "concepts.json").read_text(encoding="utf-8"))
        cls.relations = json.loads((DATA / "relations.json").read_text(encoding="utf-8"))
        cls.families = json.loads((DATA / "families.json").read_text(encoding="utf-8"))

    def test_framework_ids_are_unique(self):
        ids = [item["id"] for item in self.frameworks]
        self.assertEqual(len(ids), len(set(ids)))

    def test_csv_exports_match_canonical_json(self):
        expected = {item["id"] for item in self.frameworks}
        for relative in ("data/frameworks.csv", "docs/data/frameworks.csv"):
            with (ROOT / relative).open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(expected, {row["id"] for row in rows}, relative)
            self.assertEqual(len(expected), len(rows), relative)

    def test_relation_endpoints_exist(self):
        ids = {item["id"] for item in self.frameworks} | {item["id"] for item in self.concepts}
        for edge in self.relations:
            self.assertIn(edge["from"], ids, edge)
            self.assertIn(edge["to"], ids, edge)

    def test_deep_records_have_explanations(self):
        for item in self.frameworks:
            if item["maturity"] == "deep":
                self.assertTrue(item.get("history_ja"), item["id"])
                self.assertTrue(item.get("design_ja"), item["id"])
                self.assertTrue(item.get("data_model_ja"), item["id"])
                self.assertGreaterEqual(len(item.get("strengths_ja", [])), 2, item["id"])
                self.assertGreaterEqual(len(item.get("tradeoffs_ja", [])), 2, item["id"])
                self.assertGreaterEqual(len(item.get("sources", [])), 1, item["id"])

    def test_family_nodes_and_edges_exist(self):
        canonical = {item["id"] for item in self.frameworks} | {item["id"] for item in self.concepts}
        family_ids = set()
        for family in self.families:
            self.assertNotIn(family["id"], family_ids)
            family_ids.add(family["id"])
            virtual = {
                node["id"]
                for generation in family["generations"]
                for node in generation["nodes"]
                if node.get("virtual")
            }
            allowed = canonical | virtual
            for generation in family["generations"]:
                for node in generation["nodes"]:
                    self.assertIn(node["id"], allowed, (family["id"], node))
            for edge in family["edges"]:
                self.assertIn(edge["from"], allowed, (family["id"], edge))
                self.assertIn(edge["to"], allowed, (family["id"], edge))

    def test_site_shell_exists(self):
        for name in ("index.html", "styles.css", "app.js"):
            self.assertTrue((ROOT / "docs" / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
