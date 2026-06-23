"""
Qdrant connection and collection management.
"""

import logging

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
)

from config.settings import (
    QDRANT_HOST,
    QDRANT_PORT,
)

logger = logging.getLogger(__name__)

COLLECTION_NAME = "documents"

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
)


def check_connection() -> bool:
    """
    Check Qdrant availability.
    """

    try:
        client.get_collections()
        return True

    except Exception:
        logger.exception(
            "Unable to connect to Qdrant"
        )
        return False


def create_collection() -> None:
    """
    Create collection if it does not exist.
    """

    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME in collection_names:
        logger.info(
            "Collection already exists"
        )
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE,
        ),
    )

    logger.info(
        "Collection created successfully"
    )


def upload_points(
    points,
) -> None:
    """
    Upload points to Qdrant.
    """

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    logger.info(
        "Points uploaded: %s",
        len(points),
    )


def count_points() -> int:
    """
    Count points in collection.
    """

    result = client.count(
        collection_name=COLLECTION_NAME,
        exact=True,
    )

    return result.count


def document_exists(
    document_id: str,
) -> bool:
    """
    Check if document already exists.
    """

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id,
                    ),
                )
            ]
        ),
        limit=1,
    )

    return len(points) > 0