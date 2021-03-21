from django import forms
from pybo.models import Question, Answer


# forms.ModelForm 상속: 모델 폼 - 연결된 모델의 데이터를 저장할 수 있는 객체
#                               - 내부 클래스로 Meta클래스를 반드시 가져야 하며, Meta클래스에 모델 폼이 사용할 모델, 필드 작성
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        # form.as_p 사용 안 하고 수작업으로 HTNL코드 작성할 경우
        labels = {
            'subject':'제목',
            'content':'내용',
        }


        ''' form.as_p 사용할 경우 
        # {{ form.as_p }}태그는 form엘리먼트와 입력 항목을 자동으로 생성해주지만 부트스트랩을 적용할 수 없다는 단점이 있음
        # 부트스트랩 적용을 위해 Widgets 추가
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'context': forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        }
        # 입력받을 필드값이 한글로 표시되도록 지정
        labels = {
            'subject':'제목',
            'content':'내용',
        }
        '''

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content':'답변내용',
        }