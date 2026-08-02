#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import http.server
import json
import threading
import urllib.request

from common import ROOT


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def main() -> int:
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=ROOT / "docs", **kwargs)  # noqa: E731
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        expectations = {
            "/#family": "text/html",
            "/app.js": "text/javascript",
            "/styles.css": "text/css",
            "/data/atlas.json": "application/json",
            "/data/frameworks.csv": "text/csv",
            "/atlas-data.json": "application/json",
        }
        for path, content_type in expectations.items():
            with urllib.request.urlopen(base + path, timeout=5) as response:
                payload = response.read()
                if response.status != 200 or content_type not in response.headers.get_content_type():
                    raise RuntimeError(f"unexpected response for {path}: {response.status} {response.headers.get_content_type()}")
                if not payload:
                    raise RuntimeError(f"empty response for {path}")
                if path.endswith(".json"):
                    json.loads(payload)
        html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        script = (ROOT / "docs/app.js").read_text(encoding="utf-8")
        for marker in ("本文へ移動", "<noscript>", "Content-Security-Policy"):
            if marker not in html:
                raise RuntimeError(f"missing browser fallback marker: {marker}")
        if "データを読み込めませんでした" not in script:
            raise RuntimeError("missing corrupt/missing data user-facing error")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    print("local static-server smoke passed for HTML, JS, CSS, JSON, CSV and compatibility data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
