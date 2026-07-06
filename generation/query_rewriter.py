"""
Detection of follow-up questions and query rewriting.

Uses the existing LLM (generate_answer) to determine whether a new
question depends on the recent conversation history, and if so,
rewrites it into a standalone question.
"""

import json
import logging

from generation.generator import (
    generate_answer,
)

logger = logging.getLogger(__name__)


def _build_dependency_prompt(
    history: list[dict],
    question: str,
) -> str:
    """
    Build the prompt asking the LLM to detect dependency
    and rewrite the question if needed.
    """

    chronological_history = list(
        reversed(history)
    )

    history_block = "\n".join(
        f"User : {turn['question']}\nAssistant : {turn['answer']}"
        for turn in chronological_history
    )

    return f"""
Tu analyses une conversation pour détecter si une nouvelle question dépend du contexte des échanges précédents.

Historique :

{history_block}

Nouvelle question :

{question}

Règles :

- Si la nouvelle question peut être comprise seule, sans l'historique, elle est INDÉPENDANTE.
- Si la nouvelle question nécessite l'historique pour être comprise (ex: "Quels sont-ils ?"), elle est DÉPENDANTE.
- Si elle est dépendante, réécris-la pour qu'elle soit autonome, en intégrant le contexte nécessaire de l'historique.
- Si elle est indépendante, garde la question identique.

Réponds UNIQUEMENT avec un JSON strict, sans aucun texte autour, au format exact :

{{"is_dependent": true ou false, "rewritten_question": "..."}}
"""


def _parse_dependency_response(
    raw_response: str,
    question: str,
) -> dict:
    """
    Parse the LLM JSON response, with a safe fallback.
    """

    cleaned = raw_response.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        parsed = json.loads(cleaned)

        is_dependent = bool(
            parsed.get("is_dependent", False)
        )

        rewritten_question = parsed.get(
            "rewritten_question"
        ) or question

        return {
            "is_dependent": is_dependent,
            "rewritten_question": rewritten_question,
        }

    except (json.JSONDecodeError, AttributeError, TypeError):

        logger.warning(
            "Failed to parse dependency response, "
            "falling back to original question"
        )

        return {
            "is_dependent": False,
            "rewritten_question": question,
        }


def detect_question_dependency(
    history: list[dict],
    question: str,
) -> dict:
    """
    Determine whether `question` depends on `history`, and
    rewrite it into a standalone question if needed.

    Returns:
        {
            "is_dependent": bool,
            "rewritten_question": str,
        }
    """

    if not history:
        return {
            "is_dependent": False,
            "rewritten_question": question,
        }

    prompt = _build_dependency_prompt(
        history=history,
        question=question,
    )

    raw_response = generate_answer(
        prompt
    )

    result = _parse_dependency_response(
        raw_response=raw_response,
        question=question,
    )

    logger.info(
        "Dependency detection: is_dependent=%s",
        result["is_dependent"],
    )

    return result