"""
Convert records into Qdrant points.
"""

from uuid import UUID

from qdrant_client.models import PointStruct


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
                    UUID(
                        record["chunk_id"]
                    )
                ),
                vector=embedding,
                payload={
                    "text": record["text"],
                    **record["metadata"],
                },
            )
        )

    return points