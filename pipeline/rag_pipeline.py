"""
RAG question-answering pipeline.
"""

import logging

from retrieval.retriever import (
    retrieve_contexts,
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

    contexts = retrieve_contexts(
        query=question,
        limit=3,
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