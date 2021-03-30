from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib import messages # 오류를 임의로 발생시킬 때 사용(넌필드-입력값과 관계없이 발생한- 오류)

from .models import Post, Comment
from django.utils import timezone

from .forms import PostForm, CommentForm

from django.views import generic

def index(request):
    """게시글 목록 출력(작성일시 역순)"""
    post_list = Post.objects.order_by('-create_date')   # 기호 -가 붙어 역순

    # 페이징 처리
    page = request.GET.get('page', '1') # get방식 요청에서 page=? 형식일 때 (값이 주어지지 않을 경우 기본값 1로 설정)
    paginator = Paginator(post_list, 10) # post_list객체를 Paginator로 변환, 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'post_list':page_obj}
    return render(request, 'nboard/post_list.html', context)

# <!-- 게시글 번호(총 게시글에서의 순서)가 출력되도록 전체 게시물 개수 - 시작 인덱스 - 현재 인덱스 + 1 -->
#                 {{ post_list.paginator.count|sub:post_list.start_index|sub:forloop.counter0|add:1 }}
#                 <!-- forloop.counter0: 0부터 시작하는 루프 내의 현재 인덱스(끝에 0없으면 1부터 시작) -->



def detail(request, post_id):
    """게시글 내용 출력"""
    post = get_object_or_404(Post, pk=post_id)
    context = {'post':post}
    #'nboard/post_detail.html'
    return render(request, 'nboard/post_detail.html', context)