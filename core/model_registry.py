"""
Centralized model registry.
"""

import logging

from sentence_transformers import (
    SentenceTransformer,
)

from sentence_transformers import (
    CrossEncoder,
)

logger = logging.getLogger(__name__)

_embedding_model = None

_reranker_model = None


def get_embedding_model():
    """
    Load embedding model once.
    """

    global _embedding_model

    if _embedding_model is None:

        logger.info(
            "Loading embedding model: BAAI/bge-m3"
        )

        _embedding_model = (
            SentenceTransformer(
                "BAAI/bge-m3"
            )
        )

    return _embedding_model


def get_reranker_model():
    """
    Load reranker model once.
    """

    global _reranker_model

    if _reranker_model is None:

        logger.info(
            "Loading reranker model: BAAI/bge-reranker-v2-m3"
        )

        _reranker_model = (
            CrossEncoder(
                "BAAI/bge-reranker-v2-m3"
            )
        )

    return _reranker_model