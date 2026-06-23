"""
Streamlit UI for RAG System.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from pipeline.indexing_pipeline import (
    run_indexing_pipeline,
)

from pipeline.rag_pipeline import (
    ask,
)

import tempfile


st.set_page_config(
    page_title="RAG Assistant",
    page_icon="📚",
    layout="wide",
)


st.title(
    "📚 Local RAG Assistant"
)

st.markdown(
    "Docling + BGE-M3 + Qdrant + BGE-Reranker + Mistral 7B"
)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header(
    "Document Indexing"
)

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"],
)

if uploaded_file:

    if st.sidebar.button(
        "Index Document"
    ):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as tmp:

            tmp.write(
                uploaded_file.read()
            )

            temp_path = tmp.name

        with st.spinner(
            "Indexing document..."
        ):

            run_indexing_pipeline(
                temp_path
            )

        st.sidebar.success(
            "Document indexed successfully."
        )

# ==========================
# CHAT
# ==========================

st.subheader(
    "Ask a Question"
)

question = st.text_input(
    "Question"
)

if st.button(
    "Ask"
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Generating answer..."
        ):

            answer = ask(
                question
            )

        st.markdown(
            "## Answer"
        )

        st.write(
            answer
        )