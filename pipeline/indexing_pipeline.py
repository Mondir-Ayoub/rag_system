"""
Document indexing pipeline.
"""

import logging

from ingestion.loader import load_document
from ingestion.chunker import chunk_text
from ingestion.metadata import build_chunk_records

from embeddings.embedder import generate_embeddings

from vectorstore.qdrant_store import (
    create_collection,
)

from vectorstore.indexer import (
    prepare_points,
    upload_points,
)

logger = logging.getLogger(__name__)


def run_indexing_pipeline(
    document_path: str,
) -> None:
    """
    Complete indexing workflow.
    """

    logger.info(
        "Starting indexing pipeline"
    )

    text = load_document(
        document_path
    )

    chunks = chunk_text(
        text
    )

    records = build_chunk_records(
        chunks
    )

    embeddings = generate_embeddings(
        [
            record["text"]
            for record in records
        ]
    )

    create_collection()

    points = prepare_points(
        records,
        embeddings,
    )

    upload_points(
        points
    )

    logger.info(
        "Indexing pipeline completed"
    )