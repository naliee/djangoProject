from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login #사용자 인증, 로그인함수
from common.forms import UserForm

# Create your views here.

def signup(request):
    """계정 생성(회원 가입)"""
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)    # 회원가입 끝난 후 자동 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
