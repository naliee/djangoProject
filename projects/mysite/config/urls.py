"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pybo import views

# 페이지 요청 시 가장 먼저 호출되는 파일
# 요청 URL과 뷰 함수를 1:1로 연결해 준다.

# /(슬래시) 안붙여도 장고가 붙여줌, views.index앞에는 BASE_DIR(프로젝트 디렉터리)가 생략
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    # include: pybo/ 로 시작되는 페이지 요청은 모두 pybo/urls.py 파일에 있는 URL 매핑 참고하여 처리 
]
