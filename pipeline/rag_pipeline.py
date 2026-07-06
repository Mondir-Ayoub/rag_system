"""
RAG question-answering pipeline.
"""

import logging

from retrieval.retriever import (
    retrieve_contexts,
)

from retrieval.reranker import (
    rerank_contexts,
)

from generation.prompt_builder import (
    build_prompt,
)

from generation.generator import (
    generate_answer,
)

from generation.query_rewriter import (
    detect_question_dependency,
)

from config.settings import (
    HISTORY_TURNS,
)

logger = logging.getLogger(__name__)


def ask(
    question: str,
    history: list[dict] | None = None,
) -> dict:
    """
    Execute complete RAG workflow.

    If `history` is provided, the question is first checked for
    dependency on the recent conversation turns (HISTORY_TURNS)
    and rewritten into a standalone question if needed.
    """

    logger.info(
        "Starting RAG pipeline"
    )

    # =====================================
    # FOLLOW-UP QUESTION HANDLING
    # =====================================

    query_for_pipeline = question

    if history:

        recent_history = history[
            :HISTORY_TURNS
        ]

        dependency_result = (
            detect_question_dependency(
                history=recent_history,
                question=question,
            )
        )

        logger.info(
            "Question dependency: is_dependent=%s",
            dependency_result["is_dependent"],
        )

        query_for_pipeline = dependency_result[
            "rewritten_question"
        ]

        logger.info(
            "Query used for RAG search: %s",
            query_for_pipeline,
        )

    retrieved_contexts = (
        retrieve_contexts(
            query=query_for_pipeline,
            limit=10,
        )
    )

    logger.info(
        "Retrieved contexts: %s",
        len(retrieved_contexts),
    )

    contexts = rerank_contexts(
        question=query_for_pipeline,
        contexts=retrieved_contexts,
        top_k=5,
    )

    logger.info(
        "Reranked contexts: %s",
        len(contexts),
    )

    prompt = build_prompt(
        question=query_for_pipeline,
        contexts=contexts,
    )

    answer = generate_answer(
        prompt
    )

    logger.info(
        "RAG pipeline completed"
    )

    return {
        "answer": answer,
        "sources": contexts,
    }

# """
# RAG question-answering pipeline.
# """

# import logging

# from retrieval.retriever import (
#     retrieve_contexts,
# )

# from retrieval.reranker import (
#     rerank_contexts,
# )

# from generation.prompt_builder import (
#     build_prompt,
# )

# from generation.generator import (
#     generate_answer,
# )

# logger = logging.getLogger(__name__)


# def ask(
#     question: str,
# ) -> dict:
#     """
#     Execute complete RAG workflow.
#     """

#     logger.info(
#         "Starting RAG pipeline"
#     )

#     retrieved_contexts = retrieve_contexts(
#         query=question,
#         limit=10,
#     )

#     logger.info(
#         "Retrieved contexts: %s",
#         len(retrieved_contexts),
#     )

#     ranked_contexts = rerank_contexts(
#         question=question,
#         contexts=retrieved_contexts,
#         top_k=3,
#     )

#     logger.info(
#         "Reranked contexts: %s",
#         len(ranked_contexts),
#     )

#     # ==========================
#     # Build prompt
#     # ==========================

#     context_texts = [
#         context["text"]
#         for context in ranked_contexts
#     ]

#     prompt = build_prompt(
#         question=question,
#         contexts=context_texts,
#     )

#     answer = generate_answer(
#         prompt
#     )

#     # ==========================
#     # Build sources
#     # ==========================

#     sources = []

#     for context in ranked_contexts:

#         metadata = context.get(
#             "metadata",
#             {},
#         )

#         source = metadata.get(
#             "source_file"
#         )

#         if (
#             source
#             and source not in sources
#         ):
#             sources.append(
#                 source
#             )

#     logger.info(
#         "Sources used: %s",
#         sources,
#     )

#     logger.info(
#         "RAG pipeline completed"
#     )

#     return {
#         "answer": answer,
#         "sources": sources,
#         "contexts": ranked_contexts,
#     }