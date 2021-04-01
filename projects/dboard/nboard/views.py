from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib import messages # 오류를 임의로 발생시킬 때 사용(넌필드-입력값과 관계없이 발생한- 오류)
from django.utils import timezone

from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.views import generic

from hitcount.views import HitCountDetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
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


# LoginRequiredMixin 상속 가장 앞에 지정
class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    context_object_name = 'form'
    form_class = PostForm
    success_url = reverse_lazy('nboard:index')
    template_name = 'nboard/post_form.html'

    login_url = 'common:login'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.create_date = timezone.now()
        post.save()
        return super().form_valid(form) #super(): 부모클래스 내용 사용 (오버라이딩한 자식의 메서드가 아닌 부모의 메서드 실행)


class PostModifyView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    form_class = PostForm
    template_name = 'nboard/post_form.html'

    login_url = 'common:login'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.modify_date = timezone.now()
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        # DetailView 등에서 reverse_lazy()를 사용하며 pk를 전달하기 위해 함수 재정의
        post_id = self.kwargs['post_id'] # kwargs: n개의 변수를 함수의 인자로 보낼 때 사용
        return reverse_lazy('nboard:detail', kwargs={'post_id':post_id})



@login_required(login_url='common:login')
def post_delete(request, post_id):
    """nboard 게시글 삭제"""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, "삭제 권한이 없습니다")
        return redirect('nboard:detail', post_id=post_id)
    post.delete()
    return redirect('nboard:index')


@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    """comment 수정"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('{}#comment_{}'.format(resolve_url('nboard:detail', post_id=comment.post.id), comment.id))
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('nboard:detail', post_id=comment.post.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'comment':comment, 'form':form}
    return render(request, 'nboard/comment_form.html', context)
    

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    """comment 삭제"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제 권한이 없습니다')
    else:
        comment.delete()
    return redirect('nboard:detail', post_id=comment.post.id)


def vote_post(request, post_id):
    """게시글 추천 등록"""
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        # add함수로 데이터 추가  **ManyToManyField는 중복을 허락하지 않으므로 같은 사람이 여러 번 추천해도 수가 증가하지 않음
        post.voter.add(request.user)
    return redirect('nboard:detail', post_id=post.id)


def vote_comment(request, comment_id):
    """댓글 추천 등록"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        comment.voter.add(request.user)
    return redirect('nboard:detail', post_id=comment.post.id)

