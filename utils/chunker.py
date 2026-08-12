"""Convert statute records into small, source-addressable retrieval passages."""

from __future__ import annotations

from typing import Any


CHUNK_SIZE = 1_800
CHUNK_OVERLAP = 250


def _value(row: Any, key: str) -> str:
    value = row.get(key, "")
    return "" if value is None else str(value).strip()


def _first(row: Any, *keys: str) -> str:
    return next((value for key in keys if (value := _value(row, key))), "")


def _chunks(text: str):
    """Split exceptionally long provisions without losing an overlap for context."""
    if len(text) <= CHUNK_SIZE:
        return [text]

    chunks, start = [], 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        if end < len(text):
            split_at = max(text.rfind("\n", start, end), text.rfind(". ", start, end))
            if split_at > start + CHUNK_SIZE // 2:
                end = split_at + 1
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = end - CHUNK_OVERLAP
    return chunks


def _metadata(row: Any) -> dict[str, str | int]:
    law_title = _first(row, "law_name_en", "law_title", "law_name_bn")
    section_number = _first(row, "section_no_en", "section_no_bn")
    section_name = _first(row, "section_name_en", "article_name_en", "article_name_bn", "section_name")
    section_label = " ".join(part for part in (section_number, section_name) if part).strip()
    return {
        "law_title": law_title or "Untitled law",
        "law_title_bn": _value(row, "law_name_bn"),
        "section_number": section_number,
        "section_name": section_label or "Unnumbered provision",
        "chapter": _first(row, "chapter_name_en", "part_name_en"),
        "chapter_number": _first(row, "chapter_no_en", "part_no_en"),
        "source_file": _value(row, "source_file"),
        "source_record": int(_value(row, "source_record") or 0),
    }


def dataframe_to_documents(df):
    """Create embeddings-ready chunks and metadata from the normalized JSON rows."""
    documents, metadata = [], []

    for _, row in df.iterrows():
        meta = _metadata(row)
        content = _first(row, "content", "section_description", "article_bn")
        if not content:
            continue

        title_lines = [f"Law: {meta['law_title']}"]
        if meta["law_title_bn"]:
            title_lines.append(f"Law (Bangla): {meta['law_title_bn']}")
        if meta["chapter"]:
            title_lines.append(f"Chapter/Part: {meta['chapter']}")
        title_lines.append(f"Section/Article: {meta['section_name']}")
        header = "\n".join(title_lines)

        for chunk_number, chunk in enumerate(_chunks(content), start=1):
            documents.append(f"{header}\n\nText:\n{chunk}")
            metadata.append({**meta, "chunk_number": chunk_number})

    if not documents:
        raise ValueError("No embeddable legal text was found in the JSON files.")
    return documents, metadata
