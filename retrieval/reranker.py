# """
# Reranking retrieved chunks using BGE-Reranker-v2-M3.
# """

# import logging

# from sentence_transformers import (
#     CrossEncoder,
# )

# logger = logging.getLogger(__name__)

# _MODEL = None


# def get_reranker() -> CrossEncoder:
#     """
#     Lazy loading of reranker model.
#     """

#     global _MODEL

#     if _MODEL is None:

#         logger.info(
#             "Loading reranker model"
#         )

#         _MODEL = CrossEncoder(
#             "BAAI/bge-reranker-v2-m3"
#         )

#         logger.info(
#             "Reranker model loaded"
#         )

#     return _MODEL


# def rerank_contexts(
#     question: str,
#     contexts: list[str],
#     top_k: int = 5,
# ) -> list[str]:
#     """
#     Rerank retrieved contexts.
#     """

#     if not contexts:
#         return []

#     model = get_reranker()

#     pairs = [
#         (question, context)
#         for context in contexts
#     ]

#     scores = model.predict(
#         pairs
#     )

#     ranked = sorted(
#         zip(
#             contexts,
#             scores,
#         ),
#         key=lambda item: item[1],
#         reverse=True,
#     )

#     return [
#         context
#         for context, _
#         in ranked[:top_k]
#     ]

"""
Reranking utilities.
"""

from core.model_registry import (
    get_reranker_model,
)


def rerank_contexts(
    question: str,
    contexts: list[str],
    top_k: int = 3,
) -> list[str]:
    """
    Rerank retrieved contexts.
    """

    if not contexts:
        return []

    model = get_reranker_model()

    pairs = [
        (
            question,
            context,
        )
        for context in contexts
    ]

    scores = model.predict(
        pairs
    )

    ranked = sorted(
        zip(
            contexts,
            scores,
        ),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        context
        for context, _
        in ranked[:top_k]
    ]