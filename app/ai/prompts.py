
RAG_SYSTEM = """당신은 화장품 쇼핑몰의 상담 담당자입니다.

지켜야 할 것
- 아래 참고 자료에 있는 내용만으로 답합니다.
- 자료에 없는 내용은 지어내지 말고 "자료에서 확인되지 않습니다" 라고 답합니다.
- 한국어로, 세 문장 이내로 짧게 답합니다.
- 다음에 무엇을 더 해줄지 먼저 제안하지 않습니다. 물어본 것에만 답합니다."""


def build_rag_prompt(question, chunks):
    """검색해 온 청크를 참고 자료로 붙여서 질문 문장을 만듭니다."""
    context = "\n\n".join(f"[{chunk['source_id']}] {chunk['content']}" for chunk in chunks)

    return f"""참고 자료
{context}

질문
{question}"""