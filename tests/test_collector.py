from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from collect_github import CollectionError, GitHubClient, Window, collect, plan_windows  # noqa: E402


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def get_json(self, path: str, params: dict[str, object]) -> dict[str, object]:
        self.calls.append(params)
        if params["per_page"] == 1:
            return {"total_count": 101}
        page = int(params["page"])
        count = 100 if page == 1 else 1
        start = 0 if page == 1 else 100
        return {"items": [{"node_id": f"NODE-{index}", "full_name": f"org/repo-{index}"} for index in range(start, start + count)]}


class CollectorTests(unittest.TestCase):
    def test_overflow_window_is_recursively_partitioned(self) -> None:
        root = Window(dt.date(2020, 1, 1), dt.date(2020, 1, 4))

        def count(query: str) -> int:
            return 2001 if "2020-01-01..2020-01-04" in query else 500

        self.assertEqual(
            [Window(dt.date(2020, 1, 1), dt.date(2020, 1, 2)), Window(dt.date(2020, 1, 3), dt.date(2020, 1, 4))],
            plan_windows("framework", root, count)
        )

    def test_999_does_not_split_and_1001_does(self) -> None:
        root = Window(dt.date(2020, 1, 1), dt.date(2020, 1, 2))
        self.assertEqual([root], plan_windows("framework", root, lambda _: 999))
        windows = plan_windows("framework", root, lambda query: 1001 if "01..2020-01-02" in query else 1)
        self.assertEqual(2, len(windows))

    def test_single_day_overflow_fails_honestly(self) -> None:
        root = Window(dt.date(2020, 1, 1), dt.date(2020, 1, 1))
        with self.assertRaisesRegex(RuntimeError, "one day"):
            plan_windows("framework", root, lambda _: 1001)

    def test_collection_paginates_deduplicates_and_checkpoints(self) -> None:
        client = FakeClient()
        root = Window(dt.date(2020, 1, 1), dt.date(2020, 1, 1))
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "checkpoint.json"
            result = collect("framework", root, client, checkpoint)
            saved = json.loads(checkpoint.read_text(encoding="utf-8"))
        self.assertEqual(101, len(result["items"]))
        self.assertEqual(2, len(saved["completed"]))
        self.assertNotIn("token", saved)
        resumed = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "checkpoint.json"
            checkpoint.write_text(json.dumps(saved), encoding="utf-8")
            collect("framework", root, resumed, checkpoint)
        self.assertEqual(1, len(resumed.calls), "resume should recount the window but not repeat completed pages")

    def test_malformed_response_is_a_typed_partial_error(self) -> None:
        class MalformedClient:
            def get_json(self, path: str, params: dict[str, object]) -> dict[str, object]:
                return {"total_count": 1} if params["per_page"] == 1 else {"items": "not-an-array"}

        root = Window(dt.date(2020, 1, 1), dt.date(2020, 1, 1))
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(CollectionError) as raised:
            collect("framework", root, MalformedClient(), Path(directory) / "checkpoint.json")
        self.assertEqual("partial", raised.exception.state)

    def test_fixture_provenance_digests_match(self) -> None:
        import hashlib
        manifest = json.loads((ROOT / "tests/fixtures/manifest.json").read_text(encoding="utf-8"))
        for record in manifest["files"]:
            self.assertEqual(record["sha256"], hashlib.sha256((ROOT / record["path"]).read_bytes()).hexdigest())

    def test_rate_limit_and_upstream_failure_are_distinct(self) -> None:
        import urllib.error

        def opener(request: object, timeout: int) -> object:
            raise urllib.error.HTTPError("https://api.github.com", 429, "rate", {"Retry-After": "120"}, None)

        with self.assertRaises(CollectionError) as rate:
            GitHubClient(None, max_wait=1, max_retries=0, opener=opener).get_json("/search/repositories", {"q": "x"})
        self.assertEqual("rate_limited", rate.exception.state)
        rate.exception.__cause__.close()

        def upstream(request: object, timeout: int) -> object:
            raise urllib.error.HTTPError("https://api.github.com", 503, "upstream", {}, None)

        with self.assertRaises(CollectionError) as failure:
            GitHubClient(None, max_wait=1, max_retries=0, opener=upstream).get_json("/search/repositories", {"q": "x"})
        self.assertEqual("partial", failure.exception.state)
        failure.exception.__cause__.close()


if __name__ == "__main__":
    unittest.main()
