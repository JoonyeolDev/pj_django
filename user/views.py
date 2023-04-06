"""
장고에서 제공하는 기능을 최대한 사용해 구현해봅시다.
아래 from ... import ... 구문이 힌트입니다. 
지금은 해당 함수가 어떻게 구현되어있는지 전부다 이해 할 수는 없겠지만 
지금까지 공부한 내용으로 이해할 수 있는 부분이 있을겁니다.
모르는 부분이 있다면 지금입니다. 공부할 타이밍!
"""
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
            return redirect('/')

    elif request.method == 'GET':
        # user가 로그인 상태면 다시 홈으로 보냄
        user = request.user.is_authenticated
        if user:
            return redirect('/')
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
            return redirect('/')
    elif request.method == 'GET':
        form = AuthenticationForm()
        user = request.user.is_authenticated
        if user:
            return redirect('/')

    return render(request, 'user/signin.html', {'form': form})


@login_required
def user_logout(request):
    # 로그아웃 view
    auth.logout(request)
    return redirect('/')
