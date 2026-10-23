import streamlit as st

from src.research import search_arxiv
from src.downloader import download_paper, load_pdf
from src.chroma_store import build_vector_store
from src.rag_pipeline import create_rag

st.title("AI Research Paper Assistant")

topic = st.text_input("Enter research topic")

# -------------------------
# SEARCH PAPERS
# -------------------------

if st.button("Search Papers"):

    papers = search_arxiv(topic)

    st.session_state["papers"] = papers

    st.write("Top Papers:")

    for i, p in enumerate(papers):
        st.write(f"{i} - {p['title']}")

# -------------------------
# SELECT PAPERS
# -------------------------

if "papers" in st.session_state:

    papers = st.session_state["papers"]

    selected = st.multiselect(
        "Select papers to analyze",
        range(len(papers))
    )

    # -------------------------
    # BUILD KNOWLEDGE BASE
    # -------------------------

    if st.button("Build Knowledge Base"):

        all_docs = []

        with st.spinner("Downloading and processing papers..."):

            for i in selected:

                pdf_url = papers[i]["pdf"]

                path = download_paper(pdf_url)

                docs = load_pdf(path)

                for d in docs:
                    d.metadata["paper_title"] = papers[i]["title"]

                all_docs.extend(docs)

        db = build_vector_store(all_docs)

        rag = create_rag(db)

        st.session_state["rag"] = rag

        st.success("Knowledge base created!")

# -------------------------
# QUESTION ANSWERING
# -------------------------

if "rag" in st.session_state:

    question = st.text_input("Ask a question about the papers")

    if st.button("Get Answer"):

        answer, sources = st.session_state["rag"](question)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")

        for s in sources:
            st.write("-", s)