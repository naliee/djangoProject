from django.urls import path
from . import views

# url별칭 사용 시 타 앱과의 충돌을 막기 위해 네임스페이스(namespace) 사용
app_name = 'pybo'

urlpatterns = [
    # pybo/ 부분은 config/urls.py 파일에서 처리했으므로 ''부분만 인자로
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    # int: question_id에 숫자가 매핑된다 / name: URL에 별칭 부여(템플릿에서 별칭을 사용해서 하드코딩 없앰)
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
]