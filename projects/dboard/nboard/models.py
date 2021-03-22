from django.db import models

# Create your models here.
class Post(models.Model):
    subject = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')    # 글자수 제한 없는 데이터
    create_date = models.DateTimeField(verbose_name='등록일시')

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'nboard_post'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    class Meta:
        db_table = 'nboard_comment'
        verbose_name = '댓글'
        verbose_name_plural = "댓글"

