from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Question, Choice
from django.utils import timezone

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latestQuestion'
    def get_queryset(self):
        return  Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'poll/result.html'


def vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except Choice.DoesNotExist:
        return render(
                request,
                'poll/detail.html',
                {
                    'question': question,
                    'error_message': "You didn't select a choice",
                },
                )
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))
