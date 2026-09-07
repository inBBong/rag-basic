"""
질문과 뜻이 비슷한 글을 찾아옵니다. RAG 에서 R(Retrieval, 검색) 에 해당합니다.

직접 확인해 보기:
    python -m app.rag.retriever "건성 피부에 쓸 토너"

하는 일은 두 줄이 전부입니다.
    1. 질문을 벡터로 바꾼다
    2. 그 벡터와 가까운 청크를 찾는다

아직 LLM 은 등장하지 않습니다. 검색만으로 어디까지 되는지 먼저 봅니다.
"""

import sys

from app.ai import vector_store
from app.ai.embedder import embed_texts
from app.db import SessionLocal

TOP_K = 10


def retrieve(db, question, top_k=TOP_K):
    query_vector = embed_texts([question])[0]
    return vector_store.search(db, query_vector, top_k)


def print_results(question, results):
    print(f'질문: "{question}"')
    print()
    print("  순위  유사도  출처      섹션            내용")
    print("  " + "-" * 76)

    for rank, chunk in enumerate(results, start=1):
        section = chunk["section"] or "후기"
        body = chunk["content"].replace("\n", " ")[:34]
        print(f"  {rank:>3}  {chunk['score']:.3f}  {chunk['source_id']:<8}  {section:<14}  {body}...")


def main():
    if len(sys.argv) < 2:
        print('사용법: python -m app.rag.retriever "질문"')
        return

    question = sys.argv[1]

    db = SessionLocal()
    results = retrieve(db, question)
    db.close()

    print_results(question, results)


if __name__ == "__main__":
    main()