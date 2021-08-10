from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound
from .models import Question
from .forms import QuestionForm
from django.template import loader
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/")
def question(request):
    question_obj = Question.objects.all()
    context = {'question_objects': question_obj}
    return render(request, 'questions/questions.html', context)


@login_required(login_url="/")
def displayQuestion(request, pk):
    question_obj = Question.objects.get(id=pk)
    return render(request, 'questions/single_question.html', {'question_object': question_obj})


@login_required(login_url="/")
def createQuestion(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ReadQuestion')

    context = {'form': form}
    return render(request, 'questions/create_question.html', context)


@login_required(login_url="/")
def updateQuestion(request, pk):
    question_obj = Question.objects.get(id=pk)
    form = QuestionForm(instance=question_obj)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question_obj)
        if form.is_valid():
            form.save()
            return redirect('ReadQuestion')

    context = {'form': form}
    return render(request, 'questions/create_question.html', context)


@login_required(login_url="/")
def reportQuestion(request, pk):
    context = {}
    try :
        question_obj = Question.objects.get(dayNo=pk)
        if question_obj is None:
            context['SomethingWentWrong'] = True
            return render(request, 'users/index.html', context)

        question_obj.report += 1
        question_obj.save()
        context['Reported'] = pk
        return render(request, 'users/index.html', context)
    except Exception as e:
        context['SomethingWentWrong'] = True
        return render(request, 'users/index.html', context)


@login_required(login_url="/")
def deleteQuestion(request, pk):
    question_obj = Question.objects.get(id=pk)

    if request.method == 'POST':
        question_obj.delete()
        return redirect('ReadQuestion')

    context = {'object': question_obj}
    return render(request, 'users/index.html', context)


def error404(request, exceptions):
    context = {}
    context['error404'] = True
    template = loader.get_template("app/index.html", context)
    return HttpResponseNotFound(template.render())
    

def error500(request,*args, **argv):
    context = {}
    context['error500'] = True
    return render(request, 'users/index.html', context)


def error403(request, exceptions):
    context = {}
    context['error403'] = True
    return render(request, 'users/index.html', context)


def error400(request, exceptions):
    context = {}
    context['error400'] = True
    return render(request, 'users/index.html', context)
