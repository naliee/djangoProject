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


# Comment create, modift, delete, vote


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


def vote_comment(request, comment_id):
    """댓글 추천 등록"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        comment.voter.add(request.user)
    return redirect('nboard:detail', post_id=comment.post.id)