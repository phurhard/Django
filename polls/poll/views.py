from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Question

# Create your views here.

def index(request):
    latestQuestion = Question.objects.order_by("-pub_date")[:5]
    context = {'latestQuestion': latestQuestion}
    return render(request, 'poll/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'poll/detail.html', {'question': question})

def result(request, question_id):
    response = "You're looking at the result of question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You have voted for question %s" % question_id)
