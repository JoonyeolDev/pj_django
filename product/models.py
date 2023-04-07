from django.db import models


# Create your models here.
# model
class Product(models.Model):
    """
    상품 모델입니다.
    상품 코드, 상품 이름, 상품 설명, 상품 가격, 사이즈 필드를 가집니다.
    """
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)
    stock_quantity = models.IntegerField(default=0)

    # __str__이 있으면 출력할 때 모델 인스턴스를 읽기 쉽다
    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        # 생성될 때 stock quantity를 0으로 초기화 로직
        if self.pk is None:
            self.stock_quantity = 0
        super().save(*args, **kwargs)


# model
class Inbound(models.Model):
    """
    입고 모델입니다.
    상품, 수량, 입고 날짜, 금액 필드를 작성합니다.
    """


# model
class Outbound(models.Model):
    """
    출고 모델입니다.
    상품, 수량, 입고 날짜, 금액 필드를 작성합니다.
    """


# model
class Invetory(models.Model):
	"""
	창고의 제품과 수량 정보를 담는 모델입니다.
	상품, 수량 필드를 작성합니다.
	작성한 Product 모델을 OneToOne 관계로 작성합시다.
	"""