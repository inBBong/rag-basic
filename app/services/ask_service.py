"""
AI 에게 질문하고 답을 만듭니다. 이게 RAG 의 전부입니다.

  1. 질문과 비슷한 글을 찾는다        (Retrieval)
  2. 찾은 글을 참고 자료로 붙인다      (Augmented)
  3. AI 에게 답을 만들게 한다          (Generation)
"""

from app.ai import llm, prompts
from app.rag.retriever import retrieve


def ask(db, question):
    chunks = retrieve(db, question)

    user_prompt = prompts.build_rag_prompt(question, chunks)
    answer = llm.ask(prompts.RAG_SYSTEM, user_prompt)

    return {"question": question, "answer": answer, "sources": chunks}