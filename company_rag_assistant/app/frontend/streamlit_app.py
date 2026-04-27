# =============================================================================
# Standard Library Imports
# =============================================================================
import json

# =============================================================================
# Third-Party Imports
# =============================================================================
import requests
import streamlit as st

# =============================================================================
# Backend Configuration
# =============================================================================

BACKEND_URL = "http://backend:8000"

# =============================================================================
# Streamlit Page Setup
# =============================================================================

st.set_page_config(
    page_title="Company Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

# =============================================================================
# Session State Initialization
# =============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

# =============================================================================
# Page Header
# =============================================================================

st.title("Company Knowledge Assistant")
st.caption("Local RAG system with ChromaDB, FastAPI, Streamlit and Ollama.")

# =============================================================================
# Backend Helper Functions
# =============================================================================

def refresh_documents():
    """
    Lädt die aktuell indexierten Dokumente vom Backend und speichert sie
    im Streamlit Session State.

    Args:
        Keine.

    Returns:
        None: Aktualisiert ausschließlich `st.session_state.documents`.
    """
    try:
        docs = requests.get(f"{BACKEND_URL}/documents", timeout=120).json()
        st.session_state.documents = docs["documents"]
    except Exception as e:
        st.error(f"Could not load documents: {e}")

# =============================================================================
# Sidebar: Document Management
# =============================================================================

with st.sidebar:
    st.header("Documents")

    uploaded_file = st.file_uploader(
        "Upload document",
        type=["txt", "md", "pdf"],
    )

    if uploaded_file is not None:
        if st.button("Ingest document"):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            try:
                with st.spinner("Indexing document..."):
                    response = requests.post(
                        f"{BACKEND_URL}/ingest",
                        files=files,
                        timeout=300,
                    )

                result = response.json()

                if result.get("status") == "success":
                    st.success(f"Indexed: {result['filename']}")
                    st.json(result)
                    refresh_documents()
                else:
                    st.error(result.get("message", "Unknown error"))

            except Exception as e:
                st.error(f"Backend error: {e}")

    st.divider()

    if st.button("Refresh documents"):
        refresh_documents()

    documents = st.session_state.documents

    if documents:
        selected_doc = st.selectbox("Indexed documents", documents)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Delete"):
                response = requests.delete(
                    f"{BACKEND_URL}/documents/{selected_doc}",
                    timeout=120,
                )
                st.success(response.json()["message"])
                refresh_documents()
                st.rerun()

        with col2:
            if st.button("Reindex"):
                response = requests.post(
                    f"{BACKEND_URL}/documents/{selected_doc}/reindex",
                    timeout=300,
                )
                st.success(response.json()["message"])
    else:
        st.info("No documents loaded yet.")

    st.divider()

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# =============================================================================
# Chat History Rendering
# =============================================================================

st.subheader("Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"**{source['filename']} — Chunk {source['chunk_index']}**"
                    )
                    st.caption(
                        f"Vector distance: {round(source['score'], 3)} | "
                        f"Rerank score: {round(source.get('rerank_score') or 0, 3)}"
                    )
                    st.write(source["chunk"])

# =============================================================================
# Chat Input & Streaming Response Handling
# =============================================================================

question = st.chat_input("Ask a question about your company documents...")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        answer_placeholder = st.empty()
        answer_placeholder.markdown("*Searching knowledge base...*")

        full_answer = ""
        sources = []
        started = False

        try:
            with requests.post(
                f"{BACKEND_URL}/chat/stream",
                params={"query": question},
                stream=True,
                timeout=300,
            ) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if not line:
                        continue

                    event = json.loads(line.decode("utf-8"))
                    event_type = event.get("type")

                    if event_type == "sources":
                        sources = event.get("sources", [])

                    elif event_type == "token":
                        if not started:
                            answer_placeholder.empty()
                            started = True

                        full_answer += event.get("content", "")
                        answer_placeholder.write(full_answer)

                    elif event_type == "done":
                        break

            if sources:
                with st.expander("Sources"):
                    for source in sources:
                        st.markdown(
                            f"**{source['filename']} — Chunk {source['chunk_index']}**"
                        )

                        vector_score = source.get("score")
                        bm25_score = source.get("bm25_score")
                        rerank_score = source.get("rerank_score")
                        retrieval_source = source.get("retrieval_source", "unknown")

                        score_parts = [f"Source: {retrieval_source}"]

                        if vector_score is not None:
                            score_parts.append(
                                f"Vector distance: {round(vector_score, 3)}"
                            )

                        if bm25_score is not None:
                            score_parts.append(
                                f"BM25 score: {round(bm25_score, 3)}"
                            )

                        if rerank_score is not None:
                            score_parts.append(
                                f"Rerank score: {round(rerank_score, 3)}"
                            )

                        st.caption(" | ".join(score_parts))
                        st.write(source["chunk"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_answer,
                    "sources": sources,
                }
            )

        except Exception as e:
            st.error(f"Error: {e}")