"""
Document indexing pipeline.
"""

import logging

from pathlib import Path

from ingestion.loader import load_document

from ingestion.chunker import (
    extract_text,
    chunk_text,
)

from ingestion.semantic_chunker import (
    semantic_chunk_text,
)

from ingestion.metadata import (
    generate_document_id_from_file,
    build_chunk_records,
)

from embeddings.embedder import (
    generate_embeddings,
)

from vectorstore.indexer import (
    build_points,
)

from vectorstore.qdrant_store import (
    create_collection,
    upload_points,
    document_exists,
)

logger = logging.getLogger(__name__)


def run_indexing_pipeline(
    document_path: str,
) -> None:
    """
    Complete document indexing workflow.
    """

    logger.info(
        "Starting indexing pipeline"
    )

    create_collection()

    # =====================================
    # FAST DUPLICATE CHECK
    # =====================================

    document_id = (
        generate_document_id_from_file(
            document_path
        )
    )

    if document_exists(
        document_id
    ):
        logger.info(
            "Document already indexed"
        )
        return

    # =====================================
    # DOCUMENT NAME
    # =====================================

    document_name = Path(
        document_path
    ).name

    # =====================================
    # LOAD DOCUMENT
    # =====================================

    document = load_document(
        document_path
    )

    text = extract_text(
        document
    )

    logger.info(
        "Text length: %s",
        len(text),
    )

    # =====================================
    # CHUNKING
    # =====================================

    USE_SEMANTIC_CHUNKING = True

    if USE_SEMANTIC_CHUNKING:

        chunks = semantic_chunk_text(
            text=text,
            similarity_threshold=0.75,
            min_chunk_size=300,
        )

    else:

        chunks = chunk_text(
            text=text,
            chunk_size=512,
            chunk_overlap=100,
        )

    logger.info(
        "Chunks generated: %s",
        len(chunks),
    )

    for i, chunk in enumerate(
        chunks[:10]
    ):
        logger.info(
            "Chunk %s size=%s",
            i + 1,
            len(chunk),
        )

        logger.info(
            "Preview:\n%s\n",
            chunk[:200],
        )

    logger.info(
        "Chunking strategy: %s",
        "semantic"
        if USE_SEMANTIC_CHUNKING
        else "static",
    )

    # =====================================
    # METADATA
    # =====================================

    records = build_chunk_records(
        chunks=chunks,
        document_id=document_id,
        document_name=document_name,
    )

    logger.info(
        "Document ID: %s",
        document_id,
    )

    # =====================================
    # EMBEDDINGS
    # =====================================

    texts = [
        record["text"]
        for record in records
    ]

    embeddings = generate_embeddings(
        texts
    )

    logger.info(
        "Embeddings generated: %s",
        len(embeddings),
    )

    logger.info(
        "Embedding dimension: %s",
        len(embeddings[0]),
    )

    # =====================================
    # QDRANT POINTS
    # =====================================

    points = build_points(
        records=records,
        embeddings=embeddings,
    )

    logger.info(
        "Points prepared: %s",
        len(points),
    )

    upload_points(
        points
    )

    logger.info(
        "Indexing pipeline completed"
    )


# """
# Document indexing pipeline.
# """

# import logging
# from pathlib import Path

# from ingestion.loader import load_document

# from ingestion.chunker import (
#     extract_text,
#     chunk_text,
# )

# from ingestion.semantic_chunker import (
#     semantic_chunk_text,
# )

# from ingestion.metadata import (
#     generate_document_id,
#     build_chunk_records,
# )

# from embeddings.embedder import (
#     generate_embeddings,
# )

# from vectorstore.indexer import (
#     build_points,
# )

# from vectorstore.qdrant_store import (
#     create_collection,
#     upload_points,
#     document_exists,
# )

# logger = logging.getLogger(__name__)


# def run_indexing_pipeline(
#     document_path: str,
#     source_file: str | None = None,
# ) -> None:
#     """
#     Complete document indexing workflow.
#     """

#     logger.info(
#         "Starting indexing pipeline"
#     )

#     create_collection()

#     document = load_document(
#         document_path
#     )

#     text = extract_text(
#         document
#     )

#     logger.info(
#         "Text length: %s",
#         len(text),
#     )

#     document_id = generate_document_id(
#         text
#     )

#     if document_exists(
#         document_id
#     ):
#         logger.info(
#             "Document already indexed"
#         )
#         return

#     if source_file is None:

#         source_file = Path(
#             document_path
#         ).name

#     USE_SEMANTIC_CHUNKING = True

#     if USE_SEMANTIC_CHUNKING:

#         chunks = semantic_chunk_text(
#             text=text,
#             similarity_threshold=0.75,
#             min_chunk_size=300,
#         )

#     else:

#         chunks = chunk_text(
#             text=text,
#             chunk_size=512,
#             chunk_overlap=100,
#         )

#     logger.info(
#         "Chunks generated: %s",
#         len(chunks),
#     )

#     logger.info(
#         "Chunking strategy: %s",
#         "semantic"
#         if USE_SEMANTIC_CHUNKING
#         else "static",
#     )

#     records = build_chunk_records(
#         chunks=chunks,
#         document_id=document_id,
#         source_file=source_file,
#     )

#     logger.info(
#         "Document ID: %s",
#         document_id,
#     )

#     texts = [
#         record["text"]
#         for record in records
#     ]

#     embeddings = generate_embeddings(
#         texts
#     )

#     logger.info(
#         "Embeddings generated: %s",
#         len(embeddings),
#     )

#     logger.info(
#         "Embedding dimension: %s",
#         len(embeddings[0]),
#     )

#     points = build_points(
#         records=records,
#         embeddings=embeddings,
#     )

#     logger.info(
#         "Points prepared: %s",
#         len(points),
#     )

#     upload_points(
#         points
#     )

#     logger.info(
#         "Indexing pipeline completed"
#     )