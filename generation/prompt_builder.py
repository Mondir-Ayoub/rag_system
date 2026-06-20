"""
Build RAG prompts.
"""


def build_prompt(
    question: str,
    contexts: list[str],
) -> str:
    """
    Build prompt for Mistral.
    """

    context_block = "\n\n".join(
        contexts
    )

    return f"""
Tu es un assistant spécialisé dans la réponse à partir de documents.

Règles :

- Réponds uniquement à partir du contexte fourni.
- Si l'information n'est pas présente dans le contexte, réponds :
  "Je ne trouve pas cette information dans les documents fournis."
- Sois précis et concis.

Contexte :

{context_block}

Question :

{question}

Réponse :
"""