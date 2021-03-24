from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'common'

'''path('url패턴', 실행할 뷰(비즈니스 로직), [name='']) 형식 / auth_views를 이용할 시 as_view()로 바로 html페이지 지정'''
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'), # 경로 기본 registration/login.html이므로 따로 설정
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                    # auth_views의 LogoutView를 사용하는 것인데, as_view()를 써 줘야 html로 보여줌
    path('signup/', views.signup, name='signup'),
]