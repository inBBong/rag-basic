"""
상품 상세와 후기를 잘라서 chunks 테이블에 넣습니다.

실행: python -m pipeline.chunk
    (먼저 python -m pipeline.load_data 를 실행해 두어야 합니다)

자르는 규칙은 app/ai/chunker.py 에 있습니다.
11단계의 POST /products 도 같은 함수를 씁니다.

여러 번 실행해도 됩니다. 매번 chunks 테이블을 비우고 다시 채웁니다.
"""

from app.ai.chunker import make_product_chunks, make_review_chunk
from app.db import Base, SessionLocal, engine
from app.models.chunk import Chunk
from app.models.product import Product
from app.models.review import Review


def print_result(db):
    product_chunks = db.query(Chunk).filter(Chunk.source == "product").count()
    review_chunks = db.query(Chunk).filter(Chunk.source == "review").count()

    print("청킹 완료")
    print("  상품 상세 ->", product_chunks, "개 청크")
    print("  후기      ->", review_chunks, "개 청크")
    print("  합계      ->", product_chunks + review_chunks, "개 청크")
    print()

    sections = db.query(Chunk).filter(Chunk.source_id == "P001").all()
    print("상품 P001 은 이런 섹션으로 잘렸습니다")
    for chunk in sections:
        print("  -", chunk.section, "(", len(chunk.content), "자 )")
    print()

    print("조각 하나는 이렇게 생겼습니다")
    print(sections[0].content)


def main():
    Chunk.__table__.drop(engine, checkfirst=True)
    Base.metadata.create_all(engine)

    db = SessionLocal()
    products = db.query(Product).all()
    name_of = {product.product_id: product.name for product in products}

    for product in products:
        db.add_all(make_product_chunks(product))

    for review in db.query(Review).all():
        db.add(make_review_chunk(review, name_of[review.product_id]))

    db.commit()
    print_result(db)
    db.close()


if __name__ == "__main__":
    main()