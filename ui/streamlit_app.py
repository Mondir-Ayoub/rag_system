"""
Streamlit UI for RAG System.
"""

import sys
import tempfile
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

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="📚",
    layout="wide",
)

# ==================================================
# SESSION STATE
# ==================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# ==================================================
# HEADER
# ==================================================

st.title(
    "📚 Local RAG Assistant"
)

st.caption(
    "Docling • BGE-M3 • Qdrant • BGE-Reranker-v2 • Mistral 7B"
)

st.divider()

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("📄 Document Indexing")

    uploaded_files = st.file_uploader(
        "Upload PDF(s)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:

        if st.button(
            "🚀 Index Documents"
        ):

            progress_bar = st.progress(0)

            status_text = st.empty()

            total_files = len(
                uploaded_files
            )

            for idx, uploaded_file in enumerate(
                uploaded_files
            ):

                status_text.text(
                    f"Indexing {uploaded_file.name}"
                )

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf",
                ) as tmp:

                    tmp.write(
                        uploaded_file.read()
                    )

                    temp_path = tmp.name

                run_indexing_pipeline(
                    document_path=temp_path,
                    source_file=uploaded_file.name,
                )

                progress_bar.progress(
                    (idx + 1) / total_files
                )

            st.success(
                "Documents indexed successfully."
            )

    st.divider()

    st.header(
        "🕘 History"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Show / Hide"
        ):
            st.session_state.show_history = (
                not st.session_state.show_history
            )

    with col2:

        if st.button(
            "Clear"
        ):
            st.session_state.chat_history = []

# ==================================================
# MAIN CHAT
# ==================================================

st.subheader(
    "💬 Ask a Question"
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

            result = ask(
                question,
                history=st.session_state.chat_history,
            )

        answer = result[
            "answer"
        ]

        sources = result[
            "sources"
        ]

        st.session_state.chat_history.insert(
            0,
            {
                "question": question,
                "answer": answer,
            },
        )

        # ==========================
        # ANSWER
        # ==========================

        st.markdown(
            "## 🤖 Answer"
        )

        st.success(
            answer
        )

        # ==========================
        # SOURCES
        # ==========================

        st.markdown(
            "## 📚 Sources Used"
        )

        for idx, source in enumerate(
            sources,
            start=1,
        ):

            with st.expander(
                f"Chunk {idx}"
            ):

                st.write(
                    source
                )

# ==================================================
# HISTORY
# ==================================================

if (
    st.session_state.show_history
    and st.session_state.chat_history
):

    st.divider()

    st.subheader(
        "🕘 Conversation History"
    )

    for idx, item in enumerate(
        st.session_state.chat_history,
        start=1,
    ):

        with st.expander(
            f"Question {idx}"
        ):

            st.markdown(
                f"**Question:** {item['question']}"
            )

            st.markdown(
                f"**Answer:** {item['answer']}"
            )


# """
# Streamlit UI for RAG System.
# """

# import sys
# import tempfile
# from pathlib import Path

# import streamlit as st

# ROOT_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(str(ROOT_DIR))

# from pipeline.indexing_pipeline import (
#     run_indexing_pipeline,
# )

# from pipeline.rag_pipeline import (
#     ask,
# )

# # ==========================================================
# # PAGE
# # ==========================================================

# st.set_page_config(
#     page_title="Local RAG Assistant",
#     page_icon="📚",
#     layout="wide",
# )

# st.title("📚 Local RAG Assistant")

# st.caption(
#     "Docling • Semantic Chunking • BGE-M3 • Qdrant • BGE-Reranker • Mistral 7B"
# )

# # ==========================================================
# # SESSION
# # ==========================================================

# if "history" not in st.session_state:
#     st.session_state.history = []

# # ==========================================================
# # SIDEBAR
# # ==========================================================

# with st.sidebar:

#     st.header("📄 Documents")

#     uploaded_files = st.file_uploader(
#         "Upload PDF(s)",
#         type=["pdf"],
#         accept_multiple_files=True,
#     )

#     if uploaded_files:

#         if st.button("🚀 Index Documents"):

#             progress = st.progress(0)

#             status = st.empty()

#             total = len(uploaded_files)

#             for index, uploaded_file in enumerate(uploaded_files):

#                 status.info(
#                     f"Indexing {uploaded_file.name}"
#                 )

#                 with tempfile.NamedTemporaryFile(
#                     delete=False,
#                     suffix=".pdf",
#                 ) as tmp:

#                     tmp.write(
#                         uploaded_file.read()
#                     )

#                     path = tmp.name

#                 run_indexing_pipeline(
#                     path
#                 )

#                 progress.progress(
#                     (index + 1) / total
#                 )

#             status.success(
#                 "Indexation terminée."
#             )

#     st.divider()

#     show_history = st.checkbox(
#         "Afficher l'historique",
#         value=False,
#     )
# ####################
#     if show_history:

#         st.subheader("Historique")

#         if len(st.session_state.history) == 0:

#             st.caption(
#                 "Aucune question."
#             )

#         else:

#             for item in reversed(
#                 st.session_state.history
#             ):

#                 st.markdown(
#                     f"**❓ {item['question']}**"
#                 )

#                 st.caption(
#                     item["answer"][:150] + "..."
#                     if len(item["answer"]) > 150
#                     else item["answer"]
#                 )

# # ==========================================================
# # CHAT
# # ==========================================================

# st.subheader("💬 Ask a question")

# question = st.text_input(
#     "Question"
# )

# if st.button("Ask"):

#     if question.strip():

#         with st.spinner(
#             "Thinking..."
#         ):

#             result = ask(
#                 question
#             )

#         answer = result["answer"]

#         sources = result["sources"]

#         contexts = result["contexts"]

#         st.session_state.history.append(
#             {
#                 "question": question,
#                 "answer": answer,
#             }
#         )

#         # =============================
#         # Answer
#         # =============================

#         st.markdown("## Answer")

#         st.write(answer)

#         # =============================
#         # Sources
#         # =============================

#         st.markdown("---")

#         st.markdown("### 📚 Sources")

#         if sources:

#             for pdf in sources:

#                 st.markdown(
#                     f"📄 **{pdf}**"
#                 )

#         else:

#             st.info(
#                 "No source available."
#             )

#         # =============================
#         # Contexts
#         # =============================

#         with st.expander(
#             "🔍 Retrieved Chunks"
#         ):

#             for i, ctx in enumerate(
#                 contexts,
#                 start=1,
#             ):

#                 st.markdown(
#                     f"### Chunk {i}"
#                 )

#                 metadata = ctx.get(
#                     "metadata",
#                     {}
#                 )

#                 st.caption(
#                     f"Source : {metadata.get('source_file','Unknown')}"
#                 )

#                 st.code(
#                     ctx["text"],
#                     language="text",
#                 )

#     else:

#         st.warning(
#             "Please enter a question."
#         )