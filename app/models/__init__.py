# 이 폴더가 파이썬 패키지라는 걸 알려주는 파일입니다. 내용은 비어 있어도 됩니다.
"""
모델을 여기서 한 번에 불러옵니다.

테이블끼리 서로를 가리키고 있어서(ForeignKey), 하나만 불러오면
SQLAlchemy 가 나머지 테이블을 몰라서 오류가 납니다.
여기에 다 적어두면 하나만 불러와도 나머지가 같이 등록됩니다.
"""

from app.models.chunk import Chunk
from app.models.customer import Customer
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.review import Review