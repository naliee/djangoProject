from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    subject = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')    # 글자수 제한 없는 데이터
    '''NULL허용하려면 (...CASCADE, null=True)'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='등록일시')
    # auto_now_add=True로 등록 시간 입력 가능
    modify_date = models.DateTimeField(null=True, blank=True) # null허용, form.is_valid검사 시 값이 없어도 허용
                                                              # (어떤 조건으로든 값을 비워둘 수 있음)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'nboard_post'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
        # ForeignKey: 1:N 관계일 때 사용(하나의 Post에 여러 개의 Comment 연결 가능)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'nboard_comment'
        verbose_name = '댓글'
        verbose_name_plural = "댓글"

