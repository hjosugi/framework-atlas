from __future__ import annotations

import hashlib
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import freshness_report  # noqa: E402


class FreshnessTests(unittest.TestCase):
    def test_complete_attempt_records_separate_success_and_does_not_mutate_data(self) -> None:
        entity_path = ROOT / "data/entities.v1.json"
        before = hashlib.sha256(entity_path.read_bytes()).hexdigest()

        def repository(repo: str, token: str | None) -> dict[str, object]:
            return {"full_name": repo, "archived": False}

        with mock.patch.object(freshness_report, "github_repo", side_effect=repository), mock.patch.object(freshness_report, "probe_source", side_effect=lambda url: (200, url)):
            report, status = freshness_report.build_report()
        self.assertEqual(0, status)
        self.assertEqual("complete", report["state"])
        self.assertEqual(report["attemptedAt"], report["lastSuccessfulAt"])
        self.assertEqual(before, hashlib.sha256(entity_path.read_bytes()).hexdigest())

    def test_partial_attempt_preserves_previous_success(self) -> None:
        previous = {"lastSuccessfulAt": "2026-07-01T00:00:00Z"}
        with mock.patch.object(freshness_report, "github_repo", side_effect=urllib.error.URLError("offline")), mock.patch.object(freshness_report, "probe_source", side_effect=lambda url: (200, url)):
            report, status = freshness_report.build_report(previous)
        self.assertEqual(2, status)
        self.assertEqual("partial", report["state"])
        self.assertEqual(previous["lastSuccessfulAt"], report["lastSuccessfulAt"])
        self.assertNotEqual(report["attemptedAt"], report["lastSuccessfulAt"])


if __name__ == "__main__":
    unittest.main()
