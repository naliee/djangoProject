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

# Post create, modify, delete, vote


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


def vote_post(request, post_id):
    """게시글 추천 등록"""
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        # add함수로 데이터 추가  **ManyToManyField는 중복을 허락하지 않으므로 같은 사람이 여러 번 추천해도 수가 증가하지 않음
        post.voter.add(request.user)
    return redirect('nboard:detail', post_id=post.id)