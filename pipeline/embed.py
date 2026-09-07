"""
청크를 벡터로 바꿔서 저장합니다.

실행: python -m pipeline.embed
    (먼저 python -m pipeline.chunk 를 실행해 두어야 합니다)
    .env 에 OPENAI_API_KEY 가 필요합니다.

아직 벡터가 없는 청크만 처리합니다.
그래서 중간에 끊겨도 다시 실행하면 남은 것부터 이어서 합니다.
"""

import json
import time

from app.ai import vector_store
from app.ai.embedder import DIMENSION, MODEL, embed_texts
from app.db import SessionLocal

# 한 번에 보낼 청크 수. 하나씩 보내면 3060번을 불러야 해서 매우 느립니다.
BATCH_SIZE = 100


def embed_batch(db, chunks):
    vectors = embed_texts([chunk.content for chunk in chunks])
    vector_store.save_embeddings(db, chunks, vectors)


def main():
    db = SessionLocal()

    todo = vector_store.find_chunks_to_embed(db)
    total = vector_store.count_all(db)

    if not todo:
        print(f"이미 전부 임베딩되어 있습니다. ({total}개)")
        db.close()
        return

    print(f"전체 청크 {total}개 중 {len(todo)}개를 임베딩합니다.")
    print(f"모델 {MODEL} / {DIMENSION}차원 / 한 번에 {BATCH_SIZE}개씩")
    print()

    started = time.time()
    for start in range(0, len(todo), BATCH_SIZE):
        batch = todo[start : start + BATCH_SIZE]
        embed_batch(db, batch)

        done = min(start + BATCH_SIZE, len(todo))
        bar = "#" * (done * 30 // len(todo))
        print(f"\r  [{bar:<30}] {done}/{len(todo)}", end="")

    seconds = time.time() - started
    print()
    print()
    print(f"임베딩 완료  {len(todo)}개 / {seconds:.1f}초")
    print(f"  벡터가 있는 청크 : {vector_store.count_embedded(db)}개")

    sample = vector_store.find_first_embedded(db)
    vector = json.loads(sample.embedding)
    first_line = sample.content.splitlines()[0]
    first_five = [round(value, 4) for value in vector[:5]]

    print()
    print("  예시 :", first_line)
    print("    -> 숫자", len(vector), "개")
    print("    -> 앞 5개만 보면", first_five)

    db.close()


if __name__ == "__main__":
    main()