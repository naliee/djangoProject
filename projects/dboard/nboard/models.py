from django.db import models

class Post(Models.model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    # 해당 클래스 호출 시 표시될 내용 
    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = "게시글"

