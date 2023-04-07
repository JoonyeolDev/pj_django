from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def product_list(request):
    # 등록 된 상품의 리스트를 볼 수 있는 view
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_product = Product.objects.all()
            return render(request, 'product/product_list.html', {'product': all_product})
        else:
            return redirect('/sign-in')


@login_required
def product_create(request):
    # 상품 등록 view
    if request.method == 'POST':
        product_form = Product(request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('/product-list')

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if not user:
            return redirect('/sign-in')
        else:
            product_form = Product()
    return render(request, 'product/product_create.html', {'form': product_form})


@login_required
def outbound_create(request, product_id):
    # 상품 출고 view
    # 출고 기록 생성
    # 재고 수량 조정
    pass


@login_required
def inventory(request):
    """
    inbound_create, outbound_create view에서 만들어진 데이터를 합산합니다.
    Django ORM을 통하여 총 수량, 가격등을 계산할 수 있습니다.
    """
    # 총 입고 수량, 가격 계산
    # 총 출고 수량, 가격 계산
    pass
