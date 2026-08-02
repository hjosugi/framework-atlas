from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from normalize_snapshot import normalize  # noqa: E402


class NormalizeTests(unittest.TestCase):
    def test_node_identity_deduplicates_rename_and_preserves_alias(self) -> None:
        records = normalize([
            {"node_id": "N1", "full_name": "old/repo", "updated_at": "2025-01-01T00:00:00Z", "topics": ["router"], "snapshotTopic": "router", "owner": {"type": "Organization"}},
            {"node_id": "N1", "full_name": "new/repo", "updated_at": "2026-01-01T00:00:00Z", "topics": ["framework", "framework"], "snapshotTopic": "framework", "owner": {"type": "Organization"}}
        ])
        self.assertEqual(1, len(records))
        self.assertEqual("new/repo", records[0]["fullName"])
        self.assertEqual(["old/repo"], records[0]["aliases"])
        self.assertEqual(["framework", "router"], records[0]["topics"])
        self.assertEqual(["framework", "router"], records[0]["topicSources"])
        self.assertIn("rename-alias-preserved", records[0]["normalizationReasons"])

    def test_forks_are_retained_as_classification_input(self) -> None:
        records = normalize([{"node_id": "N2", "full_name": "fork/repo", "fork": True}])
        self.assertTrue(records[0]["isFork"])

    def test_input_order_does_not_change_normalized_bytes(self) -> None:
        import json
        source = [
            {"node_id": "N1", "full_name": "old/repo", "updated_at": "2025-01-01T00:00:00Z", "topics": ["router"]},
            {"node_id": "N1", "full_name": "new/repo", "updated_at": "2026-01-01T00:00:00Z", "topics": ["framework"]}
        ]
        first = json.dumps(normalize(source), ensure_ascii=False, sort_keys=True)
        second = json.dumps(normalize(list(reversed(source))), ensure_ascii=False, sort_keys=True)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
