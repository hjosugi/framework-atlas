from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site  # noqa: E402


class SiteTests(unittest.TestCase):
    def test_site_bundle_has_every_required_view(self) -> None:
        bundle = build_site.build()
        for key in ("entities", "relations", "claims", "unresolved", "generations", "caseStudy", "matrices", "hostAdapters", "routerMatrix", "profiles", "issues", "sourceDigests"):
            self.assertIn(key, bundle)
        targets = {mapping["target"] for mapping in bundle["caseStudy"]["mappings"]}
        self.assertEqual({"spring-boot", "fastapi", "gin", "kofun-boot"}, targets)

    def test_site_bundle_is_byte_deterministic(self) -> None:
        first = json.dumps(build_site.build(), ensure_ascii=False, sort_keys=True, indent=2)
        second = json.dumps(build_site.build(), ensure_ascii=False, sort_keys=True, indent=2)
        self.assertEqual(first, second)

    def test_html_has_accessible_fallbacks_and_strict_csp(self) -> None:
        html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        self.assertIn("Content-Security-Policy", html)
        self.assertIn("prefers-reduced-motion", (ROOT / "docs/styles.css").read_text(encoding="utf-8"))
        self.assertIn('id="relationship-list"', html)
        self.assertIn('class="skip-link"', html)

    def test_javascript_has_explicit_html_escaping_and_no_eval(self) -> None:
        script = (ROOT / "docs/app.js").read_text(encoding="utf-8")
        self.assertIn("function escapeHTML", script)
        self.assertIn("function escapeAttribute", script)
        self.assertNotIn("insertAdjacentHTML", script)
        self.assertNotIn("eval(", script)


if __name__ == "__main__":
    unittest.main()
