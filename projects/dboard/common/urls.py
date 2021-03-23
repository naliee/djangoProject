from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
                                    # 경로 기본 registration/login.html이므로 따로 설정
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
]