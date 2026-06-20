"""
LLM generation using Ollama.
"""

import logging

from ollama import chat

logger = logging.getLogger(__name__)

MODEL_NAME = "mistral"


def generate_answer(
    prompt: str,
) -> str:
    """
    Generate answer from Mistral.
    """

    logger.info(
        "Generating answer with %s",
        MODEL_NAME,
    )

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    answer = response.message.content

    logger.info(
        "Answer generated successfully"
    )

    return answer