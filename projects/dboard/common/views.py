from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login #사용자 인증, 로그인함수

from common.forms import UserForm
from django.contrib.auth.models import User

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


def detail(request):
    """회원 상세 보기(마이페이지)"""
    #user = get_object_or_404(User, pk=user_id)
    #context = {'user': user}
    # 회원이 작성한 글 목록 확인 기능을 위해 request에서 가져온 user.post해서 목록 출력하기
    return render(request, 'common/user_detail.html')

