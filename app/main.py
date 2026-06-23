"""
Application entry point.
"""

import logging

from config.settings import LOG_LEVEL

from config.logging_config import (
    configure_logging,
)

from pipeline.indexing_pipeline import (
    run_indexing_pipeline,
)

from pipeline.rag_pipeline import (
    ask,
)

from vectorstore.qdrant_store import (
    check_connection,
    count_points,
)

DOCUMENT_PATH = "documents/test.pdf"


QUESTION = (
    "Quels est le code wifi du EXCORP-GUEST ?"
)


def main() -> None:

    configure_logging(LOG_LEVEL)

    logger = logging.getLogger(__name__)

    try:

        if not check_connection():
            raise ConnectionError(
                "Unable to connect to Qdrant"
            )

        logger.info(
            "Qdrant connection successful"
        )

        run_indexing_pipeline(
            DOCUMENT_PATH
        )

        logger.info(
            "Total points in collection: %s",
            count_points(),
        )

        answer = ask(
            QUESTION
        )

        logger.info(
            "\nQUESTION:\n%s",
            QUESTION,
        )

        logger.info(
            "\nANSWER:\n%s",
            answer,
        )

    except Exception:

        logger.exception(
            "Pipeline execution failed"
        )

        raise


if __name__ == "__main__":
    main()