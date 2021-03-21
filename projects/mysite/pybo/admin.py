from django.contrib import admin
from .models import Question

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject'] #검색 기능 추가 


admin.site.register(Question, QuestionAdmin)   #관리자 페이지에 pybo.Question 추가(데이터 등록 수정 가능)