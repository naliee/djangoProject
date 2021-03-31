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


@login_required(login_url='common:login')
def post_create(request):
    """게시글 등록"""
    if request.method == 'POST':    # 내용 입력 후 등록 클릭할 경우 POST - request의 POST요청으로 들어온 폼을 저장
        form = PostForm(request.POST) 

        if form.is_valid(): # form이 유효한지 검사
            post = form.save(commit=False) # create_date는 아직 저장되지 않았으므로 임시저장
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('nboard:index')

    else: # Get요청일 경우 - 내용 등록 버튼을 눌렀을 경우 등록 form 페이지
        form = PostForm()
    context = {'form':form}
    return render(request, 'nboard/post_form.html', context)


# 로그아웃 상태일 시 request.user에는 AnonymousUser객체가 들어있어 로그아웃 상태로 해당 함수 실행 시 오류 발생
# 로그인이 필요한 로직의 경우 @login_required 어노테이션 적용 (login_url=: 로그아웃상태로 해당 함수 실행 시 이동할 URL)
# 이 방식으로 common:login으로 이동 후, 로그인 성공 시 next파라미터에 있는 URL페이지로 이동(login.html에 next파라미터 추가해줌)
@login_required(login_url='common:login')
def comment_create(request, post_id):
    """게시글 댓글 등록"""
    post = get_object_or_404(Post, pk=post_id) # 파라미터로 들어온 pk로 post데이터 가져와 저장

    if request.method == "POST":
            # POST로 받은 request값을 CommentForm으로 변환
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('nboard:detail', post_id=post_id), comment.id))
                                                #resolve_url: 실체 호출되는 url을 문자열로 반환하는 장고 함수
                        # 즉 url(post_id=post_id)#comment_[comment.id]로 redirect됨
    else:
        form = CommentForm()

    context = {'post':post, 'form':form}

    return render(request, 'nboard/post_detail.html', context)