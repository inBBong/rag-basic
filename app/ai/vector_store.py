"""
벡터를 저장합니다.

chunks 테이블을 다루는 곳은 이 파일 하나뿐입니다. (pipeline 스크립트만 예외)
SQLite 와 Supabase 의 차이를 전부 이 파일 안에 가둬 두려는 것입니다.
마지막에 Supabase 로 옮길 때 고치는 파일이 여기 하나로 끝납니다.

지금은 SQLite 라서 벡터를 JSON 문자열로 저장합니다.
"""

import json

import numpy as np

from app.models.chunk import Chunk

_chunks = None
_vectors = None


def find_chunks_to_embed(db):
    """아직 벡터가 없는 청크만 가져옵니다.

    이 함수 덕분에 나중에 증분 임베딩이 가능합니다.
    새 상품을 추가해도 그 상품의 청크만 벡터가 없으니, 그것만 임베딩하면 됩니다.
    """
    # SQLAlchemy 에서 "값이 비어 있다" 는 is None 이 아니라 is_(None) 으로 씁니다.
    return db.query(Chunk).filter(Chunk.embedding.is_(None)).all()


def save_embeddings(db, chunks, vectors):
    """청크에 벡터를 붙여 저장합니다."""
    for chunk, vector in zip(chunks, vectors):
        chunk.embedding = json.dumps(vector)
    db.commit()


def count_all(db):
    return db.query(Chunk).count()


def count_embedded(db):
    return db.query(Chunk).filter(Chunk.embedding.is_not(None)).count()


def find_first_embedded(db):
    """벡터가 어떻게 생겼는지 확인해 볼 때 씁니다."""
    return db.query(Chunk).filter(Chunk.embedding.is_not(None)).first()



def load_into_memory(db):
    """DB 의 벡터를 전부 읽어서 메모리에 올립니다. 처음 한 번만 실행됩니다."""
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



def search(db, query_vector, top_k=10):
    """질문 벡터와 뜻이 가까운 청크를 top_k 개 찾아옵니다."""
    if _vectors is None:
        load_into_memory(db)

    # 벡터들의 길이가 모두 1이라서, 곱해서 더하기만 하면 그게 곧 코사인 유사도입니다.
    # 1에 가까울수록 뜻이 비슷하고, 0에 가까울수록 상관이 없습니다.
    scores = _vectors @ np.array(query_vector, dtype=np.float32)

    best = np.argsort(-scores)[:top_k]
    return [dict(_chunks[index], score=float(scores[index])) for index in best]