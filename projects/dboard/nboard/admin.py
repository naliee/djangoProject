from django.contrib import admin

from .models import Post, Comment

# Register your models here. - 장고 admin페이지 개선

class PostAdmin(admin.ModelAdmin):
    # 제목으로 게시글 검색할 수 있도록 클래스 생성, register에 추가
    search_fields = ['subject']
    list_display = ('subject', 'content')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',)



admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
