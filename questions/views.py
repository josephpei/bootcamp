from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Question, Answer
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import QuestionForm, AnswerForm
from bootcamp.decorators import ajax_required


@login_required
def _questions(request, questions, active):
    paginator = Paginator(questions, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'questions/questions.html', {
        'nbar': 'qa',
        'questions': questions,
        'active': active
    })


@login_required
def questions(request):
    return unanswered(request)


@login_required
def answered(request):
    questions = Question.get_answered()
    return _questions(request, questions, 'answered')


@login_required
def unanswered(request):
    questions = Question.get_unanswered()
    return _questions(request, questions, 'unanswered')


@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question()
            question.user = request.user
            question.title = form.cleaned_data.get('title')
            question.description = form.cleaned_data.get('description')
            question.save()
            tags = form.cleaned_data.get('tags')
            return redirect('/questions/')
        else:
            return render(request, 'questions/ask.html', {'nbar': 'qa', 'form': form})
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'nbar': 'qa', 'form': form})


@login_required
def all(request):
    questions = Question.objects.all()
    return _questions(request, questions, 'all')


@login_required
def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(initial={'question': question})
    return render(request, 'questions/question.html', {
        'nbar': 'qa',
        'question': question,
        'form': form
    })


@login_required
def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            answer = Answer()
            answer.user = user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            return redirect(u'/questions/{0}/'.format(answer.question.pk))
        else:
            question = form.cleaned_data.get('question')
            return render(request, 'questions/question.html', {
                'nbar': 'qa',
                'question': question,
                'form': form
            })
    else:
        return redirect('/questions/')


@login_required
@ajax_required
def accept(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    user = request.user

    if answer.question.user == user:
        answer.accept()
        return HttpResponse()
    else:
        return HttpResponseForbidden()
