import requests
# from Authentication.models import Subject, Question, Answer, Level

endpoint = "http://localhost:8000/main"

quest_response = requests.get(f'{endpoint}/questions')

if quest_response.status_code == 200:
    print(quest_response.json())
else:
    print(quest_response.status_code)

