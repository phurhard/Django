import os
import django
import requests
import time
from Authentication.models import Level, Quiz, Question, Option

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interactquizz.settings')
django.setup()


easyurl = [
    "https://opentdb.com/api.php?amount=15&category=9&difficulty=easy&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=20&difficulty=easy&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=21&difficulty=easy&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=22&difficulty=easy&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=24&difficulty=easy&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=28&difficulty=easy&type=multiple"]

mediumURL = [
    "https://opentdb.com/api.php?amount=15&category=9&difficulty=medium&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=20&difficulty=medium&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=21&difficulty=medium&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=22&difficulty=medium&type=multiple"]
    # "https://opentdb.com/api.php?amount=15&category=24&difficulty=medium&type=multiple",
    # "https://opentdb.com/api.php?amount=15&category=28&difficulty=hard&type=multiple"]

hardURL = [
    "https://opentdb.com/api.php?amount=15&category=9&difficulty=hard&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=20&difficulty=hard&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=21&difficulty=hard&type=multiple",
    "https://opentdb.com/api.php?amount=15&category=22&difficulty=hard&type=multiple"
]
    # "https://opentdb.com/api.php?amount=15&category=24&difficulty=hard&type=multiple",
    # "https://opentdb.com/api.php?amount=15&category=28&difficulty=hard&type=multiple"]

# urls = [easyurl, mediumURL, hardURL]
ha = ["https://opentdb.com/api.php?amount=15&category=21&difficulty=hard&type=multiple"]
for url in ha:
    time.sleep(2)

    req = requests.get(url)
    if req.status_code == 200:
        res = req.json()
        data = res.get("results")
        # creating or get a quiz
        for res in data:
            time.sleep(5)
            level, created = Level.objects.get_or_create(name='Expert')
            level.time_limit = 15
            level.save()
            quiz, created = Quiz.objects.get_or_create(title=res['category'], level=level)
            question = Question.objects.create(
                quiz=quiz,
                level=level,
                question_text=res['question']
            )
            Option.objects.create(question=question, text=res['correct_answer'], is_correct=True),
            for ans in res['incorrect_answers']:
                Option.objects.create(question=question, text=ans, is_correct=False)
    else:
        print(f'Failed to fetch data:  {url} - {req}')


# for url in mediumURL:
#     time.sleep(2)

#     req = requests.get(url)
#     if req.status_code == 200:
#         res = req.json()
#         data = res.get("results")
#         # creating or get a quiz
#         for res in data:
#             time.sleep(5)
#             level, created = Level.objects.get_or_create(name='Intermediate')
#             level.time_limit = 15
#             level.save()
#             quiz, created = Quiz.objects.get_or_create(title=res['category'], level=level)
#             question = Question.objects.create(
#                 quiz=quiz,
#                 level=level,
#                 question_text=res['question']
#             )
#             Option.objects.create(question=question, text=res['correct_answer'], is_correct=True),
#             for ans in res['incorrect_answers']:
#                 Option.objects.create(question=question, text=ans, is_correct=False)
#     else:
#         print(f'Failed to fetch data:  {url} - {req}')

ea = ["https://opentdb.com/api.php?amount=15&category=28&difficulty=easy&type=multiple"]
for url in ea:
    time.sleep(2)

    req = requests.get(url)
    if req.status_code == 200:
        res = req.json()
        data = res.get("results")
        # creating or get a quiz
        for res in data:
            time.sleep(5)
            level, created = Level.objects.get_or_create(name='Beginner')
            level.time_limit = 15
            level.save()
            quiz, created = Quiz.objects.get_or_create(title=res['category'], level=level)
            question = Question.objects.create(
                quiz=quiz,
                level=level,
                question_text=res['question']
            )
            Option.objects.create(question=question, text=res['correct_answer'], is_correct=True),
            for ans in res['incorrect_answers']:
                Option.objects.create(question=question, text=ans, is_correct=False)
    else:
        print(f'Failed to fetch data:  {url} - {req}')
