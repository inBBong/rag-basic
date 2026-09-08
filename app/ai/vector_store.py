# 벡터를 저장하고 찾습니다.

import json

import numpy as np

from app.models.chunk import Chunk

# 벡터를 담아두는 자리입니다.
#
# 벡터 3060개를 JSON 에서 숫자로 바꾸는 데 1.2초가 걸립니다.
# 질문할 때마다 이걸 다시 하면 매번 1.2초씩 기다려야 합니다.
# 그래서 처음 한 번만 읽어서 여기 올려두고, 그다음부터는 바로 씁니다.
_chunks = None
_vectors = None


# 아직 벡터가 없는 청크만 가져옵니다.
def find_chunks_to_embed(db):
    # SQLAlchemy 에서 "값이 비어 있다" 는 is None 이 아니라 is_(None) 으로 씁니다.
    return db.query(Chunk).filter(Chunk.embedding.is_(None)).all()


# 새 청크를 저장합니다. 아직 벡터는 없습니다.
def add_chunks(db, chunks):
    db.add_all(chunks)
    db.commit()


# 청크에 벡터를 붙여 저장합니다.
def save_embeddings(db, chunks, vectors):
    for chunk, vector in zip(chunks, vectors):
        chunk.embedding = json.dumps(vector)
    db.commit()


# 메모리에 올려둔 벡터를 비웁니다.
def clear_memory():
    global _chunks, _vectors
    _chunks = None
    _vectors = None


def count_all(db):
    return db.query(Chunk).count()


def count_embedded(db):
    return db.query(Chunk).filter(Chunk.embedding.is_not(None)).count()


# 벡터가 어떻게 생겼는지 확인해 볼 때 씁니다.
def find_first_embedded(db):
    return db.query(Chunk).filter(Chunk.embedding.is_not(None)).first()


# DB 의 벡터를 전부 읽어서 메모리에 올립니다. 처음 한 번만 실행됩니다.
def load_into_memory(db):
    global _chunks, _vectors

    rows = db.query(Chunk).filter(Chunk.embedding.is_not(None)).all()

    # DB 객체를 그대로 들고 있으면 세션이 닫힌 뒤에 쓸 수 없습니다.
    # 그래서 필요한 값만 뽑아서 보통 딕셔너리로 담아둡니다.
    _chunks = [
        {
            "chunk_id": row.chunk_id,
            "source": row.source,
            "source_id": row.source_id,
            "product_id": row.product_id,
            "section": row.section,
            "content": row.content,
        }
        for row in rows
    ]
    _vectors = np.array([json.loads(row.embedding) for row in rows], dtype=np.float32)


# 질문 벡터와 뜻이 가까운 청크를 top_k 개 찾아옵니다.
def search(db, query_vector, top_k=10):
    if _vectors is None:
        load_into_memory(db)

    # 벡터들의 길이가 모두 1이라서, 곱해서 더하기만 하면 그게 곧 코사인 유사도입니다.
    # 1에 가까울수록 뜻이 비슷하고, 0에 가까울수록 상관이 없습니다.
    scores = _vectors @ np.array(query_vector, dtype=np.float32)

    best = np.argsort(-scores)[:top_k]
    return [dict(_chunks[index], score=float(scores[index])) for index in best]