"""
Chunk metadata management.
"""

import hashlib

from datetime import datetime


def generate_document_id(
    text: str,
) -> str:
    """
    Generate deterministic document id from text.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def generate_document_id_from_file(
    file_path: str,
) -> str:
    """
    Generate deterministic document id from file.
    """

    sha = hashlib.sha256()

    with open(
        file_path,
        "rb",
    ) as file:

        while True:

            chunk = file.read(
                8192
            )

            if not chunk:
                break

            sha.update(
                chunk
            )

    return sha.hexdigest()


def generate_chunk_id(
    document_id: str,
    chunk: str,
) -> str:
    """
    Generate deterministic chunk id.
    """

    content = (
        document_id + chunk
    )

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def build_chunk_records(
    chunks: list[str],
    document_id: str,
    document_name: str,
    version: str = "1.0",
) -> list[dict]:
    """
    Build chunk records with metadata.
    """

    records = []

    for index, chunk in enumerate(chunks):

        records.append(
            {
                "chunk_id": generate_chunk_id(
                    document_id,
                    chunk,
                ),
                "text": chunk,
                "metadata": {
                    "document_id": document_id,
                    "document_name": document_name,
                    "chunk_index": index,
                    "version": version,
                    "created_at": datetime.utcnow().isoformat(),
                },
            }
        )

    return records


# """
# Chunk metadata management.
# """

# import hashlib

# from datetime import datetime


# def generate_document_id(
#     text: str,
# ) -> str:
#     """
#     Generate deterministic document id.
#     """

#     return hashlib.sha256(
#         text.encode("utf-8")
#     ).hexdigest()


# def generate_chunk_id(
#     document_id: str,
#     chunk: str,
# ) -> str:
#     """
#     Generate deterministic chunk id.
#     """

#     content = document_id + chunk

#     return hashlib.sha256(
#         content.encode("utf-8")
#     ).hexdigest()


# def build_chunk_records(
#     chunks: list[str],
#     document_id: str,
#     source_file: str,
#     version: str = "1.0",
# ) -> list[dict]:
#     """
#     Build chunk records with metadata.
#     """

#     records = []

#     for index, chunk in enumerate(chunks):

#         records.append(
#             {
#                 "chunk_id": generate_chunk_id(
#                     document_id,
#                     chunk,
#                 ),
#                 "text": chunk,
#                 "metadata": {
#                     "document_id": document_id,
#                     "source_file": source_file,
#                     "chunk_index": index,
#                     "version": version,
#                     "created_at": datetime.utcnow().isoformat(),
#                 },
#             }
#         )

#     return records