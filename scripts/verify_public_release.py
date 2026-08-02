#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from common import canonical_json

OWNER = "hjosugi"
REPO = "framework-atlas"


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def fetch(url: str, attempts: int, delay: int) -> tuple[bytes, dict[str, str], str]:
    last: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(url, headers={"User-Agent": "framework-atlas-public-verifier/1", "Accept": "*/*"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                headers = {key.casefold(): value for key, value in response.headers.items()}
                return response.read(), headers, response.geturl()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(delay)
    raise RuntimeError(f"anonymous read-back failed for {url}: {last}")


def github_json(path: str, attempts: int, delay: int) -> Any:
    payload, _, _ = fetch(f"https://api.github.com{path}", attempts, delay)
    return json.loads(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Anonymously verify Pages, tag and release artifacts")
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--release-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--attempts", type=int, default=18)
    parser.add_argument("--delay", type=int, default=10)
    args = parser.parse_args()
    manifest = json.loads(args.release_manifest.read_text(encoding="utf-8"))
    if manifest["sourceCommit"] != args.source_sha or manifest["tagCommit"] != args.source_sha:
        raise RuntimeError("release manifest source/tag SHA mismatch")

    tag = github_json(f"/repos/{OWNER}/{REPO}/git/ref/tags/{urllib.parse.quote(args.version, safe='')}", args.attempts, args.delay)
    tag_sha = tag["object"]["sha"]
    if tag["object"]["type"] == "tag":
        tag_object = github_json(f"/repos/{OWNER}/{REPO}/git/tags/{tag_sha}", args.attempts, args.delay)
        tag_sha = tag_object["object"]["sha"]
    if tag_sha != args.source_sha:
        raise RuntimeError(f"tag points to {tag_sha}, expected {args.source_sha}")

    base_pages = f"https://{OWNER}.github.io/{REPO}"
    page_paths = {
        "docs/index.html": "/",
        "docs/app.js": "/app.js",
        "docs/style.css": "/style.css",
        "docs/atlas-data.json": "/atlas-data.json"
    }
    endpoints: list[dict[str, Any]] = []
    for source_path, public_path in page_paths.items():
        payload, headers, final_url = fetch(base_pages + public_path, args.attempts, args.delay)
        expected = manifest["pagesSource"][source_path]
        if digest_bytes(payload) != expected["sha256"]:
            raise RuntimeError(f"Pages digest differs for {public_path}")
        endpoints.append({"url": final_url, "bytes": len(payload), "contentType": headers.get("content-type"), "cacheControl": headers.get("cache-control"), "sha256": digest_bytes(payload)})

    query_payload, query_headers, query_url = fetch(base_pages + "/?kind=http-framework#graph", args.attempts, args.delay)
    endpoints.append({"url": query_url + "#graph", "bytes": len(query_payload), "contentType": query_headers.get("content-type"), "cacheControl": query_headers.get("cache-control"), "sha256": digest_bytes(query_payload)})
    source_payload, source_headers, source_url = fetch(base_pages + "/source.json", args.attempts, args.delay)
    deployed_source = json.loads(source_payload)
    if deployed_source["commit"] != args.source_sha:
        raise RuntimeError(f"Pages source is {deployed_source['commit']}, expected {args.source_sha}")
    endpoints.append({"url": source_url, "bytes": len(source_payload), "contentType": source_headers.get("content-type"), "cacheControl": source_headers.get("cache-control"), "sha256": digest_bytes(source_payload)})

    raw_url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{args.source_sha}/data/entities.v1.json"
    raw_payload, raw_headers, raw_final = fetch(raw_url, args.attempts, args.delay)
    json.loads(raw_payload)
    endpoints.append({"url": raw_final, "bytes": len(raw_payload), "contentType": raw_headers.get("content-type"), "cacheControl": raw_headers.get("cache-control"), "sha256": digest_bytes(raw_payload)})

    release_base = f"https://github.com/{OWNER}/{REPO}/releases/download/{args.version}"
    zip_name = manifest["zip"]["name"]
    zip_payload, zip_headers, zip_url = fetch(f"{release_base}/{zip_name}", args.attempts, args.delay)
    sums_payload, sums_headers, sums_url = fetch(f"{release_base}/{manifest['checksum']['name']}", args.attempts, args.delay)
    release_manifest_payload, release_manifest_headers, release_manifest_url = fetch(f"{release_base}/release-manifest.json", args.attempts, args.delay)
    if digest_bytes(zip_payload) != manifest["zip"]["sha256"] or len(zip_payload) != manifest["zip"]["bytes"]:
        raise RuntimeError("release ZIP hash/size differs")
    checksum_line = sums_payload.decode("utf-8").strip().split()
    if checksum_line != [manifest["zip"]["sha256"], zip_name]:
        raise RuntimeError("SHA256SUMS does not describe the release ZIP")
    if json.loads(release_manifest_payload) != manifest:
        raise RuntimeError("public release manifest differs from local manifest")
    endpoints.extend([
        {"url": zip_url, "bytes": len(zip_payload), "contentType": zip_headers.get("content-type"), "cacheControl": zip_headers.get("cache-control"), "sha256": digest_bytes(zip_payload)},
        {"url": sums_url, "bytes": len(sums_payload), "contentType": sums_headers.get("content-type"), "cacheControl": sums_headers.get("cache-control"), "sha256": digest_bytes(sums_payload)},
        {"url": release_manifest_url, "bytes": len(release_manifest_payload), "contentType": release_manifest_headers.get("content-type"), "cacheControl": release_manifest_headers.get("cache-control"), "sha256": digest_bytes(release_manifest_payload)}
    ])

    with tempfile.TemporaryDirectory(prefix="framework-atlas-public-") as directory:
        archive = Path(directory) / zip_name
        archive.write_bytes(zip_payload)
        with zipfile.ZipFile(archive) as zipped:
            zip_manifest = json.loads(zipped.read("MANIFEST.json"))
            issue_index = json.loads(zipped.read("issues/index.json"))
        if zip_manifest["sourceCommit"] != args.source_sha:
            raise RuntimeError("ZIP manifest source commit differs")
    registered: dict[int, dict[str, Any]] = {}
    page = 1
    while True:
        batch = github_json(f"/repos/{OWNER}/{REPO}/issues?state=all&per_page=100&page={page}", args.attempts, args.delay)
        registered.update({item["number"]: item for item in batch if "pull_request" not in item})
        if len(batch) < 100:
            break
        page += 1
    for record in issue_index["issues"]:
        issue = registered.get(record["number"])
        if not issue:
            raise RuntimeError(f"ZIP issue #{record['number']} is not registered")
        if digest_bytes(issue["title"].encode()) != record["titleDigest"] or digest_bytes((issue.get("body") or "").encode()) != record["bodyDigest"]:
            raise RuntimeError(f"ZIP issue digest differs for #{record['number']}")

    source_zip_url = f"https://github.com/{OWNER}/{REPO}/archive/refs/tags/{args.version}.zip"
    source_zip, source_zip_headers, source_zip_final = fetch(source_zip_url, args.attempts, args.delay)
    endpoints.append({"url": source_zip_final, "bytes": len(source_zip), "contentType": source_zip_headers.get("content-type"), "cacheControl": source_zip_headers.get("cache-control"), "sha256": digest_bytes(source_zip)})
    report = {
        "version": args.version, "verifiedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sourceCommit": args.source_sha, "tagCommit": tag_sha, "anonymous": True,
        "issueDigestCount": len(issue_index["issues"]), "endpoints": endpoints,
        "result": "verified"
    }
    args.output.write_text(canonical_json(report), encoding="utf-8")
    print(f"verified {len(endpoints)} public responses, tag {tag_sha}, and {len(issue_index['issues'])} issue digests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
