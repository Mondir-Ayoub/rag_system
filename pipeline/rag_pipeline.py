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

logger = logging.getLogger(__name__)


def ask(
    question: str,
) -> str:
    """
    Execute complete RAG workflow.
    """

    logger.info(
        "Starting RAG pipeline"
    )

    retrieved_contexts = (
        retrieve_contexts(
            query=question,
            limit=10,
        )
    )

    logger.info(
        "Retrieved contexts: %s",
        len(retrieved_contexts),
    )

    contexts = rerank_contexts(
        question=question,
        contexts=retrieved_contexts,
        top_k=3,
    )

    logger.info(
        "Reranked contexts: %s",
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
        "RAG pipeline completed"
    )

    return answer