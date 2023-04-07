from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, InboundForm
from django.contrib.auth.decorators import login_required
from django.db import transaction

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
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('/product-list')

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if not user:
            return redirect('/sign-in')
        else:
            product_form = ProductForm()
    return render(request, 'product/product_create.html', {'form': product_form})


# view
# @transaction.atomic 이 데코레이터 뭐임
# 찾아보니깐 함수내의 모든 쿼리가 성공적으로 실행되거나,
# 오류가 발생하면 롤백되어 모든 변경사항이 취소된다 함
@login_required
@transaction.atomic
def inbound_create(request, product_id):
    # 상품 입고 view
    # 입고 기록 생성
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = InboundForm(request.POST)
        print('post요청 들어옴')
        print('form.errors : ', form.errors)
        print('form.is_valid() : ', form.is_valid())
        if form.is_valid():
            # commit=False를 사용하면 인스턴스는 생성하지만 데이터베이스에 저장은 안함
            # 추가로 product를 업데이트 해주고 싶어서 했음
            inbound = form.save(commit=False)
            inbound.product = product
            inbound.save()
            return redirect('/product-list')

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if not user:
            return redirect('/sign-in')
        else:
            form = InboundForm()

    return render(request, 'product/inbound_create.html', {'form': form, 'product': product})

    # 입고 수량 조정

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
