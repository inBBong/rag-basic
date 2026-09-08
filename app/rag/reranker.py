# 검색해 온 후보 10개를 다시 줄 세워서, 진짜 답이 되는 4개만 남깁니다.

import re

from app.ai import llm, prompts


# AI 답변에서 번호만 골라냅니다. 중복이나 범위를 벗어난 값은 버립니다.
def pick_numbers(answer, count):
    numbers = []
    for text in re.findall(r"\d+", answer):
        number = int(text)
        if number < count and number not in numbers:
            numbers.append(number)
    return numbers


# AI 가 top_k 개보다 적게 골랐으면 원래 검색 순서대로 채웁니다.
def fill_up(order, count, top_k):
    for number in range(count):
        if len(order) >= top_k:
            break
        if number not in order:
            order.append(number)
    return order


def rerank(question, chunks, top_k=4):
    numbered = "\n\n".join(f"[{number}] {chunk['content']}" for number, chunk in enumerate(chunks))

    system_prompt = prompts.RERANK_SYSTEM.format(top_k=top_k)
    answer = llm.ask(system_prompt, f"질문: {question}\n\n후보\n{numbered}")

    order = pick_numbers(answer, len(chunks))
    order = fill_up(order, len(chunks), top_k)

    return [chunks[number] for number in order[:top_k]]