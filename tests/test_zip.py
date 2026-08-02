from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_zip import build_archive, inspect_archive  # noqa: E402


class ZipTests(unittest.TestCase):
    def test_two_archives_are_byte_identical_and_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "a.zip"
            second = Path(directory) / "b.zip"
            build_archive(first, "test")
            build_archive(second, "test")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            inspect_archive(first)


if __name__ == "__main__":
    unittest.main()
