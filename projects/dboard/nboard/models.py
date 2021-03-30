from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    subject = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')    # 글자수 제한 없는 데이터
    '''NULL허용하려면 (...CASCADE, null=True)'''                # voter와 같은 테이블을 참조하므로 구분하기 위해 옵션 추가
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post', verbose_name='작성자')
    create_date = models.DateTimeField(verbose_name='등록일시')
    # auto_now_add=True로 등록 시간 입력 가능
    modify_date = models.DateTimeField(null=True, blank=True, verbose_name='수정일시') # null허용, form.is_valid검사 시 값이 없어도 허용
                                                              # (어떤 조건으로든 값을 비워둘 수 있음)
    voter = models.ManyToManyField(User, related_name="voter_post", verbose_name='추천인') # 다대다 관계 - 한 사람이 여러 글 추천, 한 글에 여러 사람이 추천 가능

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'nboard_post'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='게시글')
        # ForeignKey: 1:N 관계일 때 사용(하나의 Post에 여러 개의 Comment 연결 가능)
    content = models.TextField(verbose_name='댓글내용')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment',verbose_name='작성자')
    create_date = models.DateTimeField(verbose_name='작성일시')
    modify_date = models.DateTimeField(null=True, blank=True, verbose_name='수정일시')
    voter = models.ManyToManyField(User, related_name='voter_comment', verbose_name='추천인')

    class Meta:
        db_table = 'nboard_comment'
        verbose_name = '댓글'
        verbose_name_plural = "댓글"

