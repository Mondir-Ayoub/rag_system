"""
Document chunking utilities.
"""

from typing import List


def extract_text(document) -> str:
    """
    Extract markdown text from a Docling document.
    """

    return document.export_to_markdown()


def chunk_text(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 100,
) -> List[str]:
    """
    Split text into overlapping chunks.
    """

    if not text.strip():
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += (
            chunk_size
            - chunk_overlap
        )

    return chunks