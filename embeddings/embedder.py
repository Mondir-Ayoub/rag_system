# """
# Embedding generation using BGE-M3.
# """

# import logging

# from sentence_transformers import SentenceTransformer

# logger = logging.getLogger(__name__)

# _MODEL_NAME = "BAAI/bge-m3"

# _model = None


# def get_model() -> SentenceTransformer:
#     """
#     Load embedding model once.
#     """

#     global _model

#     if _model is None:
#         logger.info(
#             "Loading embedding model: %s",
#             _MODEL_NAME,
#         )

#         _model = SentenceTransformer(
#             _MODEL_NAME
#         )

#         logger.info(
#             "Embedding model loaded"
#         )

#     return _model


# def generate_embeddings(
#     texts: list[str],
# ) -> list[list[float]]:
#     """
#     Generate embeddings in batch.
#     """

#     model = get_model()

#     vectors = model.encode(
#         texts,
#         normalize_embeddings=True,
#         show_progress_bar=True,
#     )

#     return vectors.tolist()

"""
Embedding generation utilities.
"""

from core.model_registry import (
    get_embedding_model,
)


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """
    Generate embeddings.
    """

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    return embeddings.tolist()