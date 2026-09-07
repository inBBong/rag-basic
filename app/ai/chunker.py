"""
긴 글을 검색하기 좋은 크기로 자릅니다.

이 파일은 두 곳에서 씁니다.
  pipeline/chunk.py            처음에 상품 200개를 한꺼번에 자를 때
  services/product_service.py  11단계에서 새 상품 하나를 자를 때

그래서 자르는 규칙을 여기 한 곳에만 둡니다.


자를 때 지킨 세 가지

1. 의미 단위로 자릅니다
  글자 수로 뚝 자르면 문장 중간이 끊깁니다.
  상품 상세는 "##" 로 섹션이 나뉘어 있으니 그 경계에서 자릅니다.

2. 조각마다 상품 이름을 앞에 붙입니다
  "가벼운 마무리가 필요할 때 크림 대신 사용합니다" 라는 조각만 놓고 보면
  어느 상품 이야기인지 알 수 없습니다. 그러면 "비타민C 필링 로션 사용법" 이라고
  물어봐도 찾아내지 못합니다. 이름을 붙여두면 검색이 훨씬 잘 됩니다.

3. 저장하기 전에 개인정보를 가립니다
  고객이 후기 본문에 "샘플 문의는 bomin54@example.com 로 주세요" 처럼
  연락처를 직접 적어두는 경우가 있습니다. 실제로 후기 1500건 중 137건이 그랬습니다.

  청크는 저장만 되고 끝나는 게 아니라 곧바로 임베딩 API 로 나갑니다.
  그러니 답변을 만들기 직전에 가리는 것으로는 늦습니다.
   **가장 앞에서, 저장하기 전에 가립니다.**
"""


from app.ai import masking
from app.models.chunk import Chunk


def split_detail(product_name, detail):
    """상품 상세 문서를 ## 섹션 단위로 자릅니다."""
    sections = []

    for block in detail.split("\n## "):
        block = block.strip()
        if block.startswith("## "):
            block = block[3:]  # 맨 첫 섹션에만 "## " 가 남아 있습니다
        if not block:
            continue

        title, _, body = block.partition("\n")
        title = title.strip()
        sections.append(
            {
                "section": title,
                "content": f"{product_name} - {title}\n{body.strip()}",
            }
        )

    return sections


def make_review_text(product_name, rating, content):
    """후기 한 건을 청크로 만듭니다. 후기는 짧아서 자르지 않습니다."""
    return f"{product_name} 후기 ({rating}점)\n{content}"


def make_product_chunks(product):
    """상품 하나의 상세 문서를 섹션별 청크로 만듭니다."""
    return [
        Chunk(
            source="product",
            source_id=product.product_id,
            product_id=product.product_id,
            section=section["section"],
            content=masking.mask(section["content"]),
        )
        for section in split_detail(product.name, product.detail)
    ]


def make_review_chunk(review, product_name):
    return Chunk(
        source="review",
        source_id=review.review_id,
        product_id=review.product_id,
        section=None,
        content=masking.mask(make_review_text(product_name, review.rating, review.content)),
    )