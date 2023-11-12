from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import Question
# Create your tests here.

# create a function to create question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionTestCase(TestCase):
    def test_is_published_recently_future(self):
        future = timezone.now() + datetime.timedelta(days=30)
        futureQues = Question(pub_date=future, question_text='Futures')
        self.assertIs(futureQues.is_published_recently(), False)

    def test_is_published_recently_old(self):
        old = timezone.now() - datetime.timedelta(days=1, seconds=20)
        oldQues = Question(pub_date=old)
        self.assertIs(oldQues.is_published_recently(), False)

    def test_is_published_recently_recent(self):
        recent = timezone.now() - datetime.timedelta(hours=10, minutes=50, seconds=20)
        recentQues = Question(pub_date=recent)
        self.assertIs(recentQues.is_published_recently(), True)


class ViewsTestCase(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('poll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls available')
        self.assertQuerySetEqual(response.context['latestQuestion'], [])

    def test_past_question(self):
        question = create_question(question_text='Sample question', days=-10)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerySetEqual(
                response.context['latestQuestion'], [question]
                )

    def test_future_question(self):
        question = create_question(question_text='Future questionss', days=20)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerySetEqual(response.context['latestQuestion'], [])

    def test_future_and_past_question(self):
        futureQues = create_question(question_text='future', days=30)
        oldQues = create_question(question_text='Old question', days=-10)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerySetEqual(response.context['latestQuestion'], [oldQues])

    def test_two_old_question(self):
        question_one = create_question(question_text='first one', days=-10)
        question_two = create_question(question_text='second_question', days=-20)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerySetEqual(response.context['latestQuestion'], [question_one, question_two])


class DetailTestCase(TestCase):
    def test_future_question(self):
        question = create_question(question_text='future question', days=5)
        response = self.client.get(reverse('poll:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_old_question(self):
        question = create_question(question_text='old ques', days=-4)
        response = self.client.get(reverse('poll:detail', args=(question.id,)))
        self.assertContains(response, question.question_text)


class QuestionWithChoice(TestCase):
    '''write test to not print questions without choices'''
    def test_question_no_choices(self):
        question = create_question(question_text='question with bo choice', days=-3)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerySetEqual(question.choice_set.all(), [])
