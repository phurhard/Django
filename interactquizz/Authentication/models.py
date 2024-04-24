from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    """The user model
    get's the required basic details and makes the username unique.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50)
    age = models.IntegerField()
    password = models.CharField(max_length=50)
    level = models.ForeignKey("Level", null=True, blank=True, on_delete=models.SET_NULL)
    scores = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.email} {self.username}'


class Subject(models.Model):
    """The different subjects or topics that makes up the questions"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Level(models.Model):
    """The difficulty level of the questions
    Levels can be selected as drop down or radio"""
    LEVEL = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
        ('StarLord', 'StarLord'),
    ]
    name = models.CharField(max_length=50, choices=LEVEL, default="Beginner", null=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    """The question model
    Linked to the subject and level of the question
    then the main question text"""
    subject_name = models.ForeignKey("Subject", on_delete=models.CASCADE)
    level = models.ForeignKey('Level', null=False, on_delete=models.CASCADE)
    question_text = models.TextField()
    # mark = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.question_text}'


class Answer(models.Model):
    """The answer model
    Each answer is linked to a question and can either be correct or not
    the answer are then linked to the user that selects them"""
    question = models.ForeignKey("Question", null=False, on_delete=models.CASCADE)
    options = models.CharField(max_length=250)
    correct = models.BooleanField(default=False)
    user = models.ForeignKey("CustomUser", null=True, default="", on_delete=models.CASCADE)

    def __str__(self):
        return self.options
