"""
Convert records into Qdrant points.
"""

from uuid import uuid4

from qdrant_client.models import (
    PointStruct,
)


def build_points(
    records: list[dict],
    embeddings: list[list[float]],
) -> list[PointStruct]:
    """
    Build Qdrant points.
    """

    points = []

    for record, embedding in zip(
        records,
        embeddings,
    ):
        points.append(
            PointStruct(
                id=str(
                    uuid4()
                ),
                vector=embedding,
                payload={
                    "text": record["text"],
                    "chunk_id": record["chunk_id"],
                    **record["metadata"],
                },
            )
        )

    return points