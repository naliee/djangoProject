from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator

from .forms import QuestionForm, AnswerForm

from .models import Question

# Create your views here.
# 비즈니스 로직 작성

        # request: 장고에 의해 자동으로 전달되는 HTTP 요청 객체. 사용자가 전달한 데이터를 확인할 때 사용
def index(request):
    """pybo 목록 출력"""    

    # 페이징 기능
    page = request.GET.get('page', '1')
    # question_list = Question모델을 임포트해 작성일 역순(order_by)으로 조회한 결과 데이터
    question_list = Question.objects.order_by('-create_date')

    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    '''paginator: question_list를 페이징 객체 paginator로 변환 - 페이지당 보여줄 개수 지정'''
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}  # render함수가 템플릿을 HTML로 변환하는 과정에서 사용
    return render(request, 'pybo/question_list.html', context)
    # HttpResponse: 페이지 요청에 대한 응답을 할 때 사용

    # render함수: context에 있는 Question모델 데이터 question_list를 pybo/question_list.html파일에 적용하여 HTML 코드로 변환
    # pybo/question_list.html <- 템플릿(장고의 태그를 추가로 사용할 수 있는 HTML 파일)


# URL 매핑에 있던 question_id가 인수로 전달됨
def detail(request, question_id):
        '''pybo 질문 상세 출력'''
        # question = Question.objects.get(id=question_id)
        # get_object_or_404: 존재하지 않는 페이지에 접속하면 오류 대신 404페이지를 출력하도록 함수 변경
        question = get_object_or_404(Question, pk=question_id)
        context = {'question':question}
        return render(request, 'pybo/question_detail.html', context)


# request: detail.html에서 textarea에 입력된 데이터 / question_id: URL매핑 정보값(/pybp/answer/create/2요청 시 2 입력)
def answer_create(request, question_id):
        '''pybo 질문에 답변 등록'''
        question = get_object_or_404(Question, pk=question_id)
        if request.method == "POST":
                form = AnswerForm(request.POST)
                if form.is_valid():
                        answer = form.save(commit=False)
                        answer.create_date = timezone.now()
                        answer.question = question
                        answer.save()
                        return redirect('pybo:detail', question_id=question.id)
        else:
                form = AnswerForm()
        context = {'question':question, 'form':form}
        return render(request, 'pybo/question_detail.html', context)
        #question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
        # question.answer_set: Answer모델이 Question모델을 참조하고 있으므로 사용                       
                                #content=request에서 POST형식으로 전송된 form데이터 중 name이 content인 값
        ''' answer = Answer(question=question, request.POST.get('content'), create_date=timezone.now())
            answer.save() 
            방식으로도 저장 가능(위의 방식은 Answer모델 데이터 저장을 위해 Question모델 사용, 아래 방식은 Answer모델 사용'''
        #return redirect('pybo:detail', question_id=question_id) 
        # 답변 생성 후 상세화면 호출: redirect: 함수에 전달된 값을 참고하여 페이지 이동 
        # redirect(이동할 페이지 별칭, 해당 URL에 전달해야 하는 값)


def question_create(request):
        """pybo 질문 등록"""
        # POST방식 요청: 입력값 채운 후의 요청이므로 데이터 저장
        if request.method == 'POST':  
                #QuestionForm: 질문을 등록하기 위해 사용. 장고 폼을 상속받아 만든 QuestionForm
                form = QuestionForm(request.POST)  #POST방식일 경우 request에서 전달받은 데이터로 모델 폼의 값을 채워줌
                if form.is_valid(): #form.is_valid: POST요청으로 받은 form이 유효한지 검사 (유효하지 않을 경우 폼에 오류 저장되어 화면에 전달)
                        # form으로 Question 모델 데이터 저장 
                        question = form.save(commit=False) #commit=False: 임시 저장. 현재 create_date는 폼에 없으므로 그냥 저장할 경우 오류 발생
                        question.create_date = timezone.now() # 임시저장한 question객체를 반환받아 create_date값 설정 
                        question.save() # 실제 저장
                        return redirect('pybo:index')
        # GET방식 요청일 시: 질문 등록 화면
        else:   
                form = QuestionForm()
        context = {'form':form}
        return render(request, 'pybo/question_form.html', context)