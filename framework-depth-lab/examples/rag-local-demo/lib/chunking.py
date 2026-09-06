"""Chunking utilities.

This maps to the "indexing phase" in the article:
  collect docs -> extract text -> split into chunks -> keep metadata.

Design choices:
- One chunk should cover one topic. So we split on headings first.
- We merge small paragraphs up to `max_chars`. Tiny chunks lose context.
- Each chunk gets a stable id and a content hash.
  The hash tells us later if the text changed and needs a new embedding.
"""

import hashlib
import re
from pathlib import Path


def parse_front_matter(text: str):
    """Parse simple "key: value" front matter between --- lines.

    Returns (meta dict, body text).
    """
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip()
            body = parts[2]
    return meta, body.strip()


def split_paragraphs(body: str):
    """Split text on blank lines. Drop empty parts."""
    parts = [p.strip() for p in re.split(r"\n\s*\n", body)]
    return [p for p in parts if p]


def make_chunks(doc_path: Path, max_chars: int = 300):
    """Turn one markdown file into a list of chunk records."""
    text = doc_path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    title = meta.get("title", doc_path.stem)

    # Group paragraphs under their section heading.
    grouped = []  # list of (section, text)
    section = ""
    buffer = ""
    for para in split_paragraphs(body):
        if para.startswith("#"):
            # New heading. Flush the buffer first.
            if buffer:
                grouped.append((section, buffer))
                buffer = ""
            section = para.lstrip("#").strip()
            continue
        if buffer and len(buffer) + len(para) > max_chars:
            # Buffer is full. Start a new chunk.
            grouped.append((section, buffer))
            buffer = para
        else:
            buffer = (buffer + "\n" + para).strip()
    if buffer:
        grouped.append((section, buffer))

    records = []
    for i, (section, chunk_text) in enumerate(grouped):
        # We prepend title + section before embedding.
        # A bare paragraph like "5-7 business days" is hard to match alone.
        # With context, the vector points to the right topic.
        embed_text = f"{title} / {section}\n{chunk_text}" if section else f"{title}\n{chunk_text}"
        records.append({
            "chunk_id": f"{doc_path.stem}-{i:03d}",
            "doc": doc_path.name,
            "section": section,
            "text": chunk_text,
            "embed_text": embed_text,
            "content_hash": hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()[:16],
            "meta": meta,
        })
    return records
