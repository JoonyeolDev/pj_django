from django.db import models
import datetime


# Create your models here.
# model
class Product(models.Model):
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

    # *args, **kwargs를 사용하면 나중에 메소트 호출에 추가 인수가 필요한 경우
    # 수정이 더 쉽고 코드를 변경할 필요 없이 인수 전달 가능하다
    def save(self, *args, **kwargs):
        # 생성될 때 stock quantity를 0으로 초기화 로직
        if self.pk is None:
            self.stock_quantity = 0
        super().save(*args, **kwargs)


# model
class Inbound(models.Model):
    # on_delete=models.CASCADE 해당 상품이 삭제 시 입고 정보도 삭제
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    inbound_date = models.DateField(null=True)
    inbound_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

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
    # on_delete=models.CASCADE 해당 상품이 삭제 시 입고 정보도 삭제
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    outbound_date = models.DateField(null=True)
    outbound_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

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

