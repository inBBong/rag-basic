# 상품 관련 업무 로직입니다.

from datetime import datetime

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


# 최근 등록된 신상품을 AI 에게 보낼 만큼만 추려서 돌려줍니다.
def get_new_products(db, limit=5, days=None):
    products = product_repository.find_recent(db, limit, days)
    return [
        {
            "product_id": product.product_id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "price": product.price,
            "created_at": product.created_at.strftime("%Y-%m-%d"),
        }
        for product in products
    ]


# 신상품 중 제일 비싼 것을 "추천" 할 수 있게 재료를 모아 줍니다.
def get_expensive_new_products(db, limit=3, days=None):
    products = product_repository.find_recent_expensive(db, limit, days)

    # 신상품이 하나도 없으면 뒤의 조회는 기준 상품이 없어서 할 수가 없습니다.
    if not products:
        return []

    # 맨 앞이 가장 비싼 상품입니다. 이 상품을 기준으로 근거와 대안을 모읍니다.
    top = products[0]

    rows = [
        {
            "구분": "신상품 비싼 순",
            "순위": rank,
            "product_id": product.product_id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "price": product.price,
            "skin_type": product.skin_type,
            "created_at": product.created_at.strftime("%Y-%m-%d"),
        }
        for rank, product in enumerate(products, start=1)
    ]

    # 같은 카테고리 가격대와 나란히 놓아 "얼마나 비싼 편인지" 를 숫자로 만듭니다.
    stats = product_repository.get_category_price_stats(db, top.category)
    average = round(stats.avg_price)
    rows.append(
        {
            "구분": "같은 카테고리 가격 비교",
            "category": top.category,
            "카테고리_상품수": stats.count,
            "카테고리_평균가": average,
            "카테고리_최저가": stats.min_price,
            "카테고리_최고가": stats.max_price,
            "추천상품_가격": top.price,
            # 평균의 몇 % 인지. 180% 면 "평균보다 한참 위" 라고 말할 수 있습니다.
            "평균대비": f"{round(top.price / average * 100)}%",
        }
    )

    # 숫자만 있으면 추천 문장이 건조해서 소개글을 한 줄 같이 넘깁니다.
    # detail(평균 1370자)은 너무 길어서 붙이지 않고 짧은 description 만 씁니다.
    rows.append(
        {
            "구분": "추천 상품 소개글",
            "product_id": top.product_id,
            "name": top.name,
            "description": top.description,
        }
    )

    rows += [
        {
            "구분": "같은 카테고리 더 저렴한 대안",
            "product_id": product.product_id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            # 추천 상품보다 얼마나 싼지. 그대로 "○○원 저렴" 이라고 쓸 수 있습니다.
            "가격차": top.price - product.price,
        }
        for product in product_repository.find_cheaper_in_category(db, top.category, top.price)
    ]

    return rows


# 상품 하나와, 그 상품이 몇 조각으로 잘렸는지를 같이 돌려줍니다.
def get_product_detail(db, product_id):
    product = product_repository.find_by_id(db, product_id)
    if not product:
        return None

    return {
        "product": product,
        "detail": product.detail,
        "chunks": vector_store.find_chunks_by_product(db, product_id),
        "total_chunks": vector_store.count_all(db),
    }


# 상품을 등록하고, 그 상품만 임베딩합니다.
def create_product(db, data):
    if product_repository.find_by_id(db, data.product_id):
        return None

    # ProductCreate 의 항목 이름이 Product 와 같아서 그대로 풀어 넘깁니다.
    # 등록 시각은 여기서 찍습니다. 모델에 기본값으로 두면 CSV 적재에도 걸립니다.
    product = product_repository.save(
        db, Product(**data.model_dump(), created_at=datetime.now())
    )

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