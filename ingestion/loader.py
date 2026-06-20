"""
Document loading using Docling.
"""

import logging
from pathlib import Path

from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)

_converter = DocumentConverter()


def load_document(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    logger.info(
        "Loading document: %s",
        file_path,
    )

    result = _converter.convert(file_path)

    logger.info(
        "Document extracted successfully"
    )

    return result.document