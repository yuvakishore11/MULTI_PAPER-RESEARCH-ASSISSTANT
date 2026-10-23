from dotenv import load_dotenv
import os

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


def create_rag(db):

    retriever = db.as_retriever(search_kwargs={"k":6})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
You are a research assistant.

Answer the question using the research paper excerpts.

Context:
{context}

Question:
{question}

Provide a clear answer and cite paper titles.
""")

    def ask(question):
        
        docs = retriever.invoke(question)


        context = ""
        sources = set()

        for d in docs:

            context += d.page_content + "\n\n"

            title = d.metadata.get("paper_title","Unknown")

            page = d.metadata.get("page","")

            sources.add(f"{title} (Page {page})")

        response = llm.invoke(
            prompt.format(context=context,question=question)
        )

        return response.content, sources

    return ask