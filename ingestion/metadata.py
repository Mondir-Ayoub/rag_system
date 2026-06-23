"""
Chunk metadata management.
"""

import hashlib

from datetime import datetime


def generate_document_id(
    text: str,
) -> str:
    """
    Generate deterministic document id.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def generate_chunk_id(
    document_id: str,
    chunk: str,
) -> str:
    """
    Generate deterministic chunk id.
    """

    content = (
        document_id + chunk
    )

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def build_chunk_records(
    chunks: list[str],
    document_id: str,
    version: str = "1.0",
) -> list[dict]:
    """
    Build chunk records with metadata.
    """

    records = []

    for index, chunk in enumerate(chunks):

        records.append(
            {
                "chunk_id": generate_chunk_id(
                    document_id,
                    chunk,
                ),
                "text": chunk,
                "metadata": {
                    "document_id": document_id,
                    "chunk_index": index,
                    "version": version,
                    "created_at": datetime.utcnow().isoformat(),
                },
            }
        )

    return records