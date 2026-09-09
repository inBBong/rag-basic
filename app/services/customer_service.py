"""고객 관련 업무 로직입니다."""

from app.ai import masking
from app.repositories import customer_repository, purchase_repository, review_repository



def get_customers(db, skin_type=None, limit=20):
    if skin_type:
        return customer_repository.find_by_skin_type(db, skin_type, limit)
    return customer_repository.find_all(db, limit)


# 구매액이 큰 고객을 딕셔너리 목록으로 돌려줍니다.
def get_top_spenders(db, limit=5):
    rows = customer_repository.find_top_spenders(db, limit)
    return [
        {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "city": customer.city,
            "phone": customer.phone,
            "email": customer.email,
            "total_spend": total_spend,
        }
        for customer, total_spend in rows
    ]


# 피부 타입별 고객 수를 딕셔너리 목록으로 돌려줍니다.
def count_by_skin_type(db):
    rows = customer_repository.count_by_skin_type(db)
    return [{"skin_type": skin_type, "count": count} for skin_type, count in rows]


def get_customers(db, skin_type=None, limit=20):
    if skin_type:
        return customer_repository.find_by_skin_type(db, skin_type, limit)
    return customer_repository.find_all(db, limit)




def to_purchase_row(purchase, product):
    return {
        "purchase_id": purchase.purchase_id,
        "product_id": product.product_id,
        "product_name": product.name,
        "price": product.price,
        "quantity": purchase.quantity,
        "purchased_at": purchase.purchased_at,
    }



def to_review_row(review, product):
    return {
        "review_id": review.review_id,
        "product_id": product.product_id,
        "product_name": product.name,
        "rating": review.rating,
        "content": review.content,
        "written_at": review.written_at,
    }



def to_customer_row(customer):
    return {
        "customer_id": customer.customer_id,
        "name": customer.name,
        "gender": customer.gender,
        "age": customer.age,
        "skin_type": customer.skin_type,
        "phone": customer.phone,
        "email": customer.email,
        "city": customer.city,
        "joined_at": customer.joined_at,
    }



# 고객 한 명의 정보와 구매 내역, 후기를 모읍니다.
def get_customer_detail(db, customer_id):
    customer = customer_repository.find_by_id(db, customer_id)
    if not customer:
        return None
    purchases = [
        to_purchase_row(purchase, product)
        for purchase, product in purchase_repository.find_by_customer(db, customer_id)
    ]
    reviews = [
        to_review_row(review, product)
        for review, product in review_repository.find_by_customer(db, customer_id)
    ]
    row = to_customer_row(customer)
    return {
        "customer": row,
        # 4단계에서 만든 마스킹을 그대로 씁니다.
        "masked": masking.mask_rows([row])[0],
        "purchases": purchases,
        "reviews": reviews,
        "total_spend": sum(item["price"] * item["quantity"] for item in purchases),
    }