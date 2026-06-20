"""
Chunk metadata management.
"""

from datetime import datetime
from uuid import uuid4


def generate_document_id() -> str:
    """
    Generate a unique document id.
    """

    return str(uuid4())


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
                "chunk_id": str(uuid4()),
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