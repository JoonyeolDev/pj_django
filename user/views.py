from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def signup(request):
    # 회원 가입 view
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # 유효성 검사
        if form.is_valid():
            user = form.save()
            # 회원가입 후 로그인 상태로 만들어줌
            login(request, user)
            return redirect('/product-list')

    elif request.method == 'GET':
        # user가 로그인 상태면 다시 홈으로 보냄
        user = request.user.is_authenticated
        if user:
            return redirect('/product-list')
        else:
            form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})


def user_login(request):
    # 로그인 view
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/product-list')
    elif request.method == 'GET':
        form = AuthenticationForm()
        user = request.user.is_authenticated
        if user:
            return redirect('/product-list')

    return render(request, 'user/signin.html', {'form': form})


@login_required
def user_logout(request):
    # 로그아웃 view
    auth.logout(request)
    return redirect('/')
