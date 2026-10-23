def summarize_paper(llm, docs):
    
    text = " ".join([d.page_content for d in docs[:5]])

    prompt = f"""
Summarize the following research paper:

{text}
"""

    summary = llm.invoke(prompt)

    return summary.content