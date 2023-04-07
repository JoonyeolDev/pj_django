from django.db import models
import datetime

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
    # on_delete=models.CASCADE 해당 상품이 삭제 시 입고 정보도 삭제
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    inbound_date = models.DateField(null=True)
    inbound_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # 출력 시 상품 이름, 입고 날짜, 입고 가격, 입고 수량 표시
    def __str__(self):
        return f"{self.product.name}\n{self.inbound_date}\n개당 {self.inbound_price} 원\n{self.quantity} 개 입고"

    # 저장 시 Product.stock_quantity 에 추가
    def save(self, *args, **kwargs):
        if self.pk is None:  # Inbound 객체가 처음 생성되는 경우
            self.product.stock_quantity += self.quantity
        else:  # Inbound 객체가 업데이트되는 경우
            old_inbound = Inbound.objects.get(pk=self.pk)
            self.product.stock_quantity += self.quantity - old_inbound.quantity
        # product.stock_quantity 바꿨으니깐 저장
        self.product.save()
        super().save(*args, **kwargs)


# model
class Outbound(models.Model):
    """
    출고 모델입니다.
    상품, 수량, 입고 날짜, 금액 필드를 작성합니다.
    """
    # on_delete=models.CASCADE 해당 상품이 삭제 시 입고 정보도 삭제
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    outbound_date = models.DateField(null=True)
    outbound_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # 출력 시 상품 이름, 입고 날짜, 입고 가격, 입고 수량 표시
    def __str__(self):
        return f"{self.product.name}\n{self.outbound_date}\n개당 {self.outbound_price} 원\n{self.quantity} 개 출고"

    # 저장 시 Product.stock_quantity 에 추가
    def save(self, *args, **kwargs):
        if self.pk is None:  # Inbound 객체가 처음 생성되는 경우
            # 수량이 음수가 되지 않도록 조치
            if self.product.stock_quantity - self.quantity >= 0:
                self.product.stock_quantity -= self.quantity
        else:  # Inbound 객체가 업데이트되는 경우
            old_outbound = Outbound.objects.get(pk=self.pk)
            updated_quantity = self.quantity - old_outbound.quantity
            if updated_quantity > 0:
                self.product.stock_quantity -= updated_quantity
        # product.stock_quantity 바꿨으니깐 저장
        self.product.save()
        super().save(*args, **kwargs)


# model
class Invetory(models.Model):
    """
    창고의 제품과 수량 정보를 담는 모델입니다.
    상품, 수량 필드를 작성합니다.
    작성한 Product 모델을 OneToOne 관계로 작성합시다.
    """
    pass
