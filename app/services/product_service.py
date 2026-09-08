# 상품 관련 업무 로직입니다.

from app.ai import vector_store
from app.ai.chunker import make_product_chunks
from app.ai.embedder import embed_texts
from app.models.product import Product
from app.repositories import product_repository, purchase_repository


def get_products(db, category=None, limit=20):
    if category:
        return product_repository.find_by_category(db, category, limit)
    return product_repository.find_all(db, limit)


# 많이 팔린 상품을 딕셔너리 목록으로 돌려줍니다.
def get_best_selling(db, limit=5):
    rows = purchase_repository.find_best_selling(db, limit)
    return [
        {
            "product_id": product.product_id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "sold": sold,
        }
        for product, sold in rows
    ]


# 카테고리에 속한 상품을 AI 에게 보낼 만큼만 추려서 돌려줍니다.
def get_product_summaries(db, category, limit=10):
    products = product_repository.find_by_category(db, category, limit)
    return [
        {
            "product_id": product.product_id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "skin_type": product.skin_type,
        }
        for product in products
    ]


# 상품을 등록하고, 그 상품만 임베딩합니다.
def create_product(db, data):
    if product_repository.find_by_id(db, data.product_id):
        return None

    # ProductCreate 의 항목 이름이 Product 와 같아서 그대로 풀어 넘깁니다.
    product = product_repository.save(db, Product(**data.model_dump()))

    chunks = make_product_chunks(product)
    vector_store.add_chunks(db, chunks)

    vectors = embed_texts([chunk.content for chunk in chunks])
    vector_store.save_embeddings(db, chunks, vectors)

    # 메모리에 올려둔 벡터가 옛것이 되었으니 비웁니다. 다음 검색 때 다시 읽어옵니다.
    vector_store.clear_memory()

    total = vector_store.count_all(db)
    print(f"[증분 임베딩] 전체 청크 {total}개 중 새로 만든 {len(chunks)}개만 임베딩했습니다.")

    return {
        "product_id": product.product_id,
        "name": product.name,
        "new_chunks": len(chunks),
        "total_chunks": total,
    }