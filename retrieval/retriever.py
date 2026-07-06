"""
Vector retrieval from Qdrant.
"""

from vectorstore.qdrant_store import (
    client,
    COLLECTION_NAME,
)

from embeddings.embedder import (
    generate_embeddings,
)


def search(
    query: str,
    limit: int = 3,
) -> list[dict]:
    """
    Search relevant chunks.
    """

    query_vector = generate_embeddings(
        [query]
    )[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    )

    matches = []

    for point in results.points:

        matches.append(
            {
                "score": point.score,
                "text": point.payload["text"],
                "metadata": {
                    key: value
                    for key, value
                    in point.payload.items()
                    if key != "text"
                },
            }
        )

    return matches


def retrieve_contexts(
    query: str,
    limit: int = 3,
) -> list[str]:
    """
    Retrieve only chunk texts.
    """

    results = search(
        query=query,
        limit=limit,
    )

    return [
        result["text"]
        for result in results
    ]


# """
# Vector retrieval from Qdrant.
# """

# from vectorstore.qdrant_store import (
#     client,
#     COLLECTION_NAME,
# )

# from embeddings.embedder import (
#     generate_embeddings,
# )


# def search(
#     query: str,
#     limit: int = 3,
# ) -> list[dict]:
#     """
#     Search relevant chunks.
#     """

#     query_vector = generate_embeddings(
#         [query]
#     )[0]

#     results = client.query_points(
#         collection_name=COLLECTION_NAME,
#         query=query_vector,
#         limit=limit,
#     )

#     matches = []

#     for point in results.points:

#         metadata = {
#             key: value
#             for key, value in point.payload.items()
#             if key != "text"
#         }

#         matches.append(
#             {
#                 "score": point.score,
#                 "text": point.payload["text"],
#                 "metadata": metadata,
#             }
#         )

#     return matches


# def retrieve_contexts(
#     query: str,
#     limit: int = 3,
# ) -> list[dict]:
#     """
#     Retrieve chunks with metadata.
#     """

#     return search(
#         query=query,
#         limit=limit,
#     )