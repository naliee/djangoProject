from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Post
from django.utils import timezone

from .forms import PostForm, CommentForm

# Create your views here.
def index(request):
    """게시글 목록 출력(작성일시 역순)"""
    post_list = Post.objects.order_by('-create_date')   # 기호 -가 붙어 역순

    # 페이징 처리
    page = request.GET.get('page', '1') # get방식 요청에서 page=? 형식일 때 (값이 주어지지 않을 경우 기본값 1로 설정)
    paginator = Paginator(post_list, 10) # post_list객체를 Paginator로 변환, 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'post_list':page_obj}
    return render(request, 'nboard/post_list.html', context)


def detail(request, post_id):
    """게시글 내용 출력"""
    post = get_object_or_404(Post, pk=post_id)
    context = {'post':post}
    return render(request, 'nboard/post_detail.html', context)


def comment_create(request, post_id):
    """게시글 댓글 등록"""
    post = get_object_or_404(Post, pk=post_id) # 파라미터로 들어온 pk로 post데이터 가져와 저장

    if request.method == "POST":
            # POST로 받은 request값을 CommentForm으로 변환
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('nboard:detail', post_id=post_id)
    else:
        form = CommentForm()

    context = {'post':post, 'form':form}
    ''' form을 사용하지 않을 경우 저장법
    post.comment_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # Post모델을 통해 Comment모델 데이터를 생성하기 위해 post(post_id로 불러온 Post모델 객체).comment_set.create
    # Comment모델로 저장: comment = Comment(post=post, content=request.POST.get('content'), create_date.../ comment.save())
    return redirect('nboard:detail', post_id=post_id) # 게시글 상세 페이지로 재이동
          # redirect(): 함수에 전달된 값을 참고하여 페이지 이동: redirect(이동할 페이지 별칭, 해당 URL에 전달해야 할 값)
    '''
    return render(request, 'nboard/post_detail.html', context)


def post_create(request):
    """게시글 등록"""
    if request.method == 'POST':    # 내용 입력 후 등록 클릭할 경우 POST - request의 POST요청으로 들어온 폼을 저장
        form = PostForm(request.POST) 

        if form.is_valid(): # form이 유효한지 검사
            post = form.save(commit=False) # create_date는 아직 저장되지 않았으므로 임시저장
            post.create_date = timezone.now()
            post.save()
            return redirect('nboard:index')

    else: # Get요청일 경우 - 내용 등록 버튼을 눌렀을 경우 등록 form 페이지
        form = PostForm()
    context = {'form':form}
    return render(request, 'nboard/post_form.html', context)
