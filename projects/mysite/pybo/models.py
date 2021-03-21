from django.db import models

# Create your models here.

class Question(models.Model):
    subject = models.CharField(max_length=200) # CharField: 글자 수 제한하고 싶을 경우 사용
    content = models.TextField()               # TextField: 글자 수 제한 없는 데이터
    create_date = models.DateTimeField()       # DateTimeField: 시간 관련 속성

    # 데이터 조회 시 제목 표시(__str__문자열로 반환할 때 호출되는 함수)
    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = "질문"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Question모델을 속성으로 가져야 하기 때문에 참조키(ForeignKey) 사용
    # on_delete=models.CASCADE: 답변에 연결된 질문(Question)이 삭제되면 답변도 함께 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
