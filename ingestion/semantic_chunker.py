"""
Structure-aware semantic chunking.

Strategy:
1. Detect Docling markdown sections (#, ##, ### ...)
2. Keep small sections intact
3. Split large sections semantically
"""

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from embeddings.embedder import generate_embeddings


def split_by_paragraphs(
    text: str,
) -> list[str]:

    return [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]


def semantic_split(
    paragraphs: list[str],
    embeddings,
    threshold: float = 0.75,
    min_size: int = 300,
) -> list[str]:
    """
    Semantic split inside one section.
    """

    if len(paragraphs) == 1:
        return paragraphs

    chunks = []

    current_chunk = [
        paragraphs[0]
    ]

    current_embedding = embeddings[0]

    for i in range(
        1,
        len(paragraphs),
    ):
        similarity = cosine_similarity(
            [current_embedding],
            [embeddings[i]],
        )[0][0]

        current_text = "\n\n".join(
            current_chunk
        )

        if (
            similarity >= threshold
            or len(current_text) < min_size
        ):
            current_chunk.append(
                paragraphs[i]
            )

            current_embedding = np.mean(
                [
                    current_embedding,
                    embeddings[i],
                ],
                axis=0,
            )

        else:
            chunks.append(
                "\n\n".join(
                    current_chunk
                )
            )

            current_chunk = [
                paragraphs[i]
            ]

            current_embedding = embeddings[i]

    chunks.append(
        "\n\n".join(
            current_chunk
        )
    )

    return chunks


def semantic_chunk_text(
    text: str,
    similarity_threshold: float = 0.75,
    min_chunk_size: int = 300,
) -> list[str]:
    """
    Structure-aware semantic chunking.
    """

    lines = text.splitlines()

    sections = []

    current_title = None

    current_content = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):

            if current_content:

                sections.append(
                    (
                        current_title,
                        "\n\n".join(
                            current_content
                        ),
                    )
                )

                current_content = []

            current_title = stripped

        else:

            current_content.append(
                stripped
            )

    if current_content:

        sections.append(
            (
                current_title,
                "\n\n".join(
                    current_content
                ),
            )
        )

    if not sections:

        sections = [
            (
                None,
                text,
            )
        ]

    final_chunks = []

    for title, section_text in sections:

        paragraphs = split_by_paragraphs(
            section_text
        )

        if not paragraphs:
            continue

        if len(section_text) < (
            min_chunk_size * 2
        ):

            if title:

                final_chunks.append(
                    f"{title}\n\n{section_text}"
                )

            else:

                final_chunks.append(
                    section_text
                )

            continue

        embeddings = generate_embeddings(
            paragraphs
        )

        sub_chunks = semantic_split(
            paragraphs=paragraphs,
            embeddings=embeddings,
            threshold=similarity_threshold,
            min_size=min_chunk_size,
        )

        for chunk in sub_chunks:

            if title:

                final_chunks.append(
                    f"{title}\n\n{chunk}"
                )

            else:

                final_chunks.append(
                    chunk
                )

    return final_chunks