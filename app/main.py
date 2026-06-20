"""
Application entry point.
"""

import logging

from config.settings import LOG_LEVEL
from config.logging_config import configure_logging

from ingestion.loader import load_document

from ingestion.chunker import (
    extract_text,
    chunk_text,
)

from ingestion.metadata import (
    generate_document_id,
    build_chunk_records,
)

from embeddings.embedder import (
    generate_embeddings,
)

from vectorstore.indexer import (
    build_points,
)

from vectorstore.qdrant_store import (
    check_connection,
    create_collection,
    upload_points,
    count_points,
)

from retrieval.retriever import (
    retrieve_contexts,
)

from generation.prompt_builder import (
    build_prompt,
)

from generation.generator import (
    generate_answer,
)


DOCUMENT_PATH = "documents/test.pdf"


def main() -> None:
    """
    Main application workflow.
    """

    configure_logging(LOG_LEVEL)

    logger = logging.getLogger(__name__)

    try:
        logger.info(
            "Starting RAG indexing pipeline"
        )

        # -------------------------
        # Qdrant connection
        # -------------------------

        if not check_connection():
            raise ConnectionError(
                "Unable to connect to Qdrant"
            )

        logger.info(
            "Qdrant connection successful"
        )

        # -------------------------
        # Load document
        # -------------------------

        document = load_document(
            DOCUMENT_PATH
        )

        # -------------------------
        # Extract text
        # -------------------------

        text = extract_text(
            document
        )

        logger.info(
            "Text length: %s",
            len(text),
        )

        # -------------------------
        # Chunking
        # -------------------------

        chunks = chunk_text(
            text=text,
            chunk_size=512,
            chunk_overlap=100,
        )

        logger.info(
            "Chunks generated: %s",
            len(chunks),
        )

        # -------------------------
        # Metadata
        # -------------------------

        document_id = (
            generate_document_id()
        )

        records = build_chunk_records(
            chunks=chunks,
            document_id=document_id,
        )

        logger.info(
            "Document ID: %s",
            document_id,
        )

        # -------------------------
        # Embeddings
        # -------------------------

        texts = [
            record["text"]
            for record in records
        ]

        embeddings = (
            generate_embeddings(
                texts
            )
        )

        logger.info(
            "Embeddings generated: %s",
            len(embeddings),
        )

        logger.info(
            "Embedding dimension: %s",
            len(embeddings[0]),
        )

        # -------------------------
        # Qdrant points
        # -------------------------

        points = build_points(
            records=records,
            embeddings=embeddings,
        )

        logger.info(
            "Points prepared: %s",
            len(points),
        )

        # -------------------------
        # Collection
        # -------------------------

        create_collection()

        # -------------------------
        # Upload
        # -------------------------

        upload_points(
            points
        )

        logger.info(
            "Indexation completed"
        )

        logger.info(
            "Total points in collection: %s",
            count_points(),
        )

        # -------------------------
        # RAG Retrieval + Generation
        # -------------------------

        question = (
            "Quels sont les horaires de travail ?"
        )

        contexts = retrieve_contexts(
            question,
            limit=3,
        )

        logger.info(
            "Contexts retrieved: %s",
            len(contexts),
        )

        prompt = build_prompt(
            question=question,
            contexts=contexts,
        )

        answer = generate_answer(
            prompt
        )

        logger.info(
            "\nQUESTION:\n%s",
            question,
        )

        logger.info(
            "\nANSWER:\n%s",
            answer,
        )

    except Exception:
        logger.exception(
            "Pipeline execution failed"
        )
        raise


if __name__ == "__main__":
    main()

