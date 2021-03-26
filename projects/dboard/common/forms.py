from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# UserCreationForm 기본 속성: username, password1, password2(비밀번호 확인) 
class UserForm(UserCreationForm):
    # UserCreationForm 기본 속성에 email 추가
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username","email",) #입력받을 필드 지정 - ?기본 속성으로 username, pw1, pw2 갖고 있으므로 생략 가능?