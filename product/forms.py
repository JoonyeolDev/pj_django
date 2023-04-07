from django import forms
from .models import Product, Inbound, Outbound


# form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # stock_quantity를 제외한 나머지 필드값 모두 넣기
        # 이렇게하면 나중에 필드가 추가되더라도 자동으로 포함되서 유지관리에 유리
        exclude = ['stock_quantity']


# form
class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product', 'quantity', 'inbound_date', 'inbound_price']
        # 위젯을 이용하면 date를 정할 때 달력으로 할 수 있다
        widgets = {
            'inbound_date': forms.DateInput(attrs={'type': 'date'}),
        }


# form
class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product', 'quantity', 'outbound_date', 'outbound_price']
        # 위젯을 이용하면 date를 정할 때 달력으로 할 수 있다
        widgets = {
            'outbound_date': forms.DateInput(attrs={'type': 'date'}),
        }
