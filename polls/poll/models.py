from django.db import models
import datetime
from django.contrib import admin
from django.utils import timezone
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('publication date')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?"
    )
    def is_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
