from django.urls import path
from . import views

app_name = 'nboard'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('<int:post_id>/', views.DetailView.as_view(), name='detail'),
    path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/modify/<int:post_id>/', views.post_modify, name='post_modify'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('vote/post/<int:post_id>/', views.vote_post, name='vote_post'),
    path('vote/comment/<int:comment_id>/', views.vote_comment, name='vote_comment'),
]