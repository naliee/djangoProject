from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib import messages # 오류를 임의로 발생시킬 때 사용(넌필드-입력값과 관계없이 발생한- 오류)
from django.utils import timezone

from ..models import Post, Comment
from ..forms import PostForm, CommentForm

from django.views import generic

from hitcount.views import HitCountDetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# index, detail view

class PostListView(generic.ListView):
    paginate_by = 10
    model = Post
    #context_object_name = 'post_list'       DEFAULT : <model_name>_list
    template_name = 'nboard/post_list.html' #DEFAULT : <app_label>/<model_name>_list.html

    # ListView의 get_queryset을 오버라이딩 한 것. 이 함수는 자동실행(?)
    # queryset = Post.object...로 쓸 수도 있으나, 이 방법으로 쓰면 처음 실행시만 쿼리를 불러와 수정 후 프로세스를 재실행시켜줘야 반영됨
    def get_queryset(self):
        post_list = Post.objects.order_by('-create_date')
        return post_list


class DetailView(HitCountDetailView):
    model = Post
    count_hit = True  #조회수 추가 (쳄플릿에 hitcount로 사용) 
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    template_name = 'nboard/post_detail.html'