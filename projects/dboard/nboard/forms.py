from django import forms
from nboard.models import Post, Comment

# ModelForm: 모델과 연결한 폼 - 이 객체를 저장하면 연결된 모델의 데이터를 저장 가능
class PostForm(forms.ModelForm):
    # 메타 클래스(모델, 필드 포함) 반드시 가져야 함
    class Meta:
        model = Post
        fields = ['subject', 'content']

        # 폼에 부트스트랩 적용
        widgets = {
            'subject': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        }

        # 라벨 속성 수정하여 필드명 한글로 표기
        labels = {
            'subject':'제목',
            'content':'내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'답변 내용',
        }

