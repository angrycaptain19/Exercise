from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from pytz import utc

from .models import Question, Answer
from .forms import AnswerForm, QuestionForm
import datetime


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def question_list(request):
    page_num = request.GET.get('page', 1)
    questions = Question.objects.all()
    paginator = Paginator(questions, 10)
    page_of_questions = paginator.get_page(page_num)
    content = {'questions': page_of_questions.object_list,
               'questions_len': questions.count(),
               'page_of_questions': page_of_questions}
    curr_page_num = page_of_questions.number
    page_list_nums = list(range(max(1, curr_page_num - 2), curr_page_num)) + list(
        range(curr_page_num, min(curr_page_num + 3, paginator.num_pages + 1)))
    if page_list_nums[0] != 1:
        page_list_nums.insert(0, '...')
        page_list_nums.insert(0, 1)
    if page_list_nums[-1] != paginator.num_pages:
        page_list_nums.append('...')
        page_list_nums.append(paginator.num_pages)
    content['page_list_nums'] = page_list_nums
    content['curr_page_num'] = curr_page_num
    return render(request, 'question_list.html', content)


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    data = {'question_pk': pk}
    answer_form = AnswerForm(initial=data)
    content = {'question': question, 'answers': answers, 'answer_form': answer_form}
    return render(request, 'question_detail.html', content)


def answer_list(request):
    page_num = request.GET.get('page', 1)
    user = request.user
    answers = Answer.objects.filter(student=user)
    paginator = Paginator(answers, 10)
    page_of_answers = paginator.get_page(page_num)
    content = {'answers': page_of_answers.object_list,
               'answers_len': answers.count(),
               'page_of_answers': page_of_answers}
    curr_page_num = page_of_answers.number
    page_list_nums = list(range(max(1, curr_page_num - 2), curr_page_num)) + list(
        range(curr_page_num, min(curr_page_num + 3, paginator.num_pages + 1)))
    if page_list_nums[0] != 1:
        page_list_nums.insert(0, '...')
        page_list_nums.insert(0, 1)
    if page_list_nums[-1] != paginator.num_pages:
        page_list_nums.append('...')
        page_list_nums.append(paginator.num_pages)
    content['page_list_nums'] = page_list_nums
    content['curr_page_num'] = curr_page_num
    return render(request, 'answer_list.html', content)


def answer_detail(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    content = {'answer': answer}
    return render(request, 'answer_detail.html', content)


def update_answer(request):
    answer_form = AnswerForm(request.POST)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': '您当前未在登录状态'})
    if not answer_form.is_valid():
        return render(request, 'error.html', {'message': answer_form.errors})

    # 检查通过保存数据
    referer = request.META.get('HTTP_REFERER', '/ex')
    question = Question.objects.get(pk=answer_form.cleaned_data['question_pk'])
    now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
    deadline = question.deadline.replace(tzinfo=utc)
    answer = Answer()
    answer.isTimeout = now_time > deadline
    answer.student = request.user
    answer.answer_text = answer_form.cleaned_data['answer_text']
    answer.question = question
    answer.save()
    return redirect(referer)


def question_upload(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if not request.user.is_authenticated:
            return render(request, 'error.html', {'message': '您当前未在登录状态'})
        elif request.user.last_name != 'teacher':
            return render(request, 'error.html', {'message': 'b（￣▽￣）d　，不是老师怎么跑到这里来的'})
        if question_form.is_valid():
            # 通过检查保存数据
            teacher = request.user
            question = Question()
            question.title = question_form.cleaned_data['title']
            question.question_text = question_form.cleaned_data['question_text']
            question.deadline = question_form.cleaned_data['deadline']
            question.teacher = teacher
            question.save()
            return redirect('/ex')
        else:
            content = {'question_form': question_form}
            return render(request, 'question_upload.html', content)
    else:
        question_form = QuestionForm()
        content = {'question_form': question_form}
        return render(request, 'question_upload.html', content)
