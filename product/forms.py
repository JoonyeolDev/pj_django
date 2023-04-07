from django import forms
from product.models import Product


# form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # stock_quantity를 제외한 나머지 필드값 모두 넣기
        # 이렇게하면 나중에 필드가 추가되더라도 자동으로 포함되서 유지관리에 유리
        exclude = ['stock_quantity']


# form
class InboundForm(forms.ModelForm):
    """
    Django로 개발을 할때,
    Model과 Form을 사용하지 않으면 Django를 사용하는 의미가 없다고 말할 정도로
    Model과 Form은 Django의 핵심 기능 입니다.
    Form의 사용방법을 익혀 봅시다.
    """


# form
class OutboundForm(forms.ModelForm):
    pass