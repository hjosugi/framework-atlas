from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from classify import classify  # noqa: E402
from common import load_json  # noqa: E402


class ClassifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rules = load_json("data/rules/classification.v1.json")
        self.fixtures = json.loads((ROOT / "tests/fixtures/classifier.json").read_text(encoding="utf-8"))["repositories"]

    def test_exact_false_positive_overrides_are_reason_coded(self) -> None:
        expected = {
            "getlantern/lantern": "network-router-vpn", "threat9/routersploit": "security-exploit",
            "istoreos/istoreos": "router-os", "alibaba/ARouter": "android-navigation"
        }
        for repository in self.fixtures[:4]:
            result = classify(repository, self.rules)
            self.assertEqual("quarantined", result["disposition"])
            self.assertEqual(expected[repository["fullName"]], result["reasonCode"])
            self.assertEqual(1, result["classifierVersion"])

    def test_candidates_are_never_auto_promoted(self) -> None:
        for repository in self.fixtures[4:]:
            self.assertEqual("review_required", classify(repository, self.rules)["disposition"])


if __name__ == "__main__":
    unittest.main()
