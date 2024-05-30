import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny)


from Authentication.models import (
    Answer,
    Option,
    Question,
    Quiz,
    CustomUser,
    Level,
    Score
)
# from .models import CustomUser as User

from .serializers import (
    AnswerSerializer,
    QuestionSerializer,
    QuizSerializer,
    ScoreSerializer,
    OptionSerializer,
    UserSerializer)


class QuestionViewList(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        '''
        Creates a new question object'''
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        '''it'll return all the question objects
        available on the server'''

        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)


class QuestionViewDetail(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        '''If a primary is provided, it'll get the specific question object
        otherwise'''
        if pk:
            try:
                question = Question.objects.get(pk=pk)
                serializer = QuestionSerializer(question)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except Question.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Unable to retrieve such question'
                }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        '''
        Updates a question object'''
        serializer = QuestionSerializer(request.data)
        try:
            question = Question.objects.get(pk=pk)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                question.objects.update(**validated_data)
            return Response({
                'success': True,
                'data': serializer.data
                }, status=status.HTTP_202_ACCEPTED)
        except Question.DoesNotExist:
            return Response({
                'success': False,
                'data': serializer.errors,
                }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        '''
        deletes a specific question object, provided by the question tag'''
        serializer = QuestionSerializer(request.data)
        try:
            question = Question.objects.get(pk=pk)
            question.delete()
            return Response({
                'success': True,
                'data': serializer.data
                }, status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response({
                'success': False,
                'data': serializer.errors,
                }, status=status.HTTP_404_NOT_FOUND)


class AnswerViewList(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        '''
        Creates a new question object'''
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        '''it'll return all the question objects
        available on the server'''

        answer = Answer.objects.all()
        serializer = AnswerSerializer(answer, many=True)
        return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)


class AnswerViewDetail(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        '''If a primary is provided, it'll get the specific question object
        otherwise'''
        if pk:
            try:
                answer = Answer.objects.get(pk=pk)
                serializer = AnswerSerializer(answer)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except Answer.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Unable to retrieve such question'
                }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        '''
        Updates a question object'''
        serializer = AnswerSerializer(request.data)
        try:
            answer = Answer.objects.get(pk=pk)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                answer.objects.update(**validated_data)
            return Response({
                'success': True,
                'data': serializer.data
                }, status=status.HTTP_202_ACCEPTED)
        except Answer.DoesNotExist:
            return Response({
                'success': False,
                'data': serializer.errors,
                }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        '''
        deletes a specific question object, provided by the question tag'''
        serializer = AnswerSerializer(request.data)
        try:
            answer = Answer.objects.get(pk=pk)
            answer.delete()
            return Response({
                'success': True,
                'data': serializer.data
                }, status=status.HTTP_204_NO_CONTENT)
        except Answer.DoesNotExist:
            return Response({
                'success': False,
                'data': serializer.errors,
                }, status=status.HTTP_404_NOT_FOUND)


class ScoreViewList(APIView):
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        '''
        Creates a new question object'''
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        '''it'll return all the question objects
        available on the server'''

        scores = Score.objects.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)


class ScoreViewDetail(APIView):
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        '''If a primary is provided, it'll get the specific score object
        otherwise'''
        if pk:
            try:
                score = Score.objects.get(pk=pk)
                serializer = ScoreSerializer(score)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except Score.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Unable to retrieve such question'
                }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        '''
        Updates a question object'''
        serializer = ScoreSerializer(request.data)
        try:
            score = Score.objects.get(pk=pk)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                score.objects.update(**validated_data)
            return Response({
                'success': True,
                'data': serializer.data
                }, status=status.HTTP_202_ACCEPTED)
        except Score.DoesNotExist:
            return Response({
                'success': False,
                'data': serializer.errors,
                }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        '''
        deletes a specific question object, provided by the question tag'''
        serializer = ScoreSerializer(request.data)
        try:
            score = Score.objects.get(pk=pk)
            score.delete()
            return Response({
                'success': True,
                'data': serializer.data
                }, status=status.HTTP_204_NO_CONTENT)
        except Score.DoesNotExist:
            return Response({
                'success': False,
                'data': serializer.errors,
                }, status=status.HTTP_404_NOT_FOUND)


class QuizView(APIView):
    '''
    Only an admin account can create a quiz'''
    serializer_class = QuizSerializer
    # permission_classes = [IsAdminUser]

    def post(self, request):
        '''
        This creates a new quiz'''
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            quiz = Quiz.objects.create(**validated_data)
            serializer = QuizSerializer(quiz)
            return Response({
                'success': True,
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'data': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        '''
        This returns all quizes'''
        serializer = QuizSerializer()
        quizes = Quiz.objects.all()
        serialized_data = serializer(quizes, many=True)
        return Response({
            'success': True,
            'data': serialized_data.data,
        }, status=status.HTTP_201_CREATED)
        


# class QuizViewDetail(APIView):
#     serializer_class = QuizSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         '''If a primary is provided, it'll get the specific score object
#         otherwise'''
#         if pk:
#             try:
#                 quiz = Quiz.objects.get(pk=pk)
#                 serializer = QuizSerializer(quiz)
#                 return Response({
#                     'success': True,
#                     'data': serializer.data
#                 }, status=status.HTTP_200_OK)
#             except Quiz.DoesNotExist:
#                 return Response({
#                     'success': False,
#                     'message': 'Unable to retrieve such question'
#                 }, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         '''
#         Updates a question object'''
#         serializer = QuizSerializer(request.data)
#         try:
#             score = Quiz.objects.get(pk=pk)
#             if serializer.is_valid():
#                 validated_data = serializer.validated_data
#                 score.objects.update(**validated_data)
#             return Response({
#                 'success': True,
#                 'data': serializer.data
#                 }, status=status.HTTP_202_ACCEPTED)
#         except Quiz.DoesNotExist:
#             return Response({
#                 'success': False,
#                 'data': serializer.errors,
#                 }, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk):
#         '''
#         deletes a specific question object, provided by the question tag'''
#         serializer = QuizSerializer(request.data)
#         try:
#             quiz = Quiz.objects.get(pk=pk)
#             quiz.delete()
#             return Response({
#                 'success': True,
#                 'data': serializer.data
#                 }, status=status.HTTP_204_NO_CONTENT)
#         except Quiz.DoesNotExist:
#             return Response({
#                 'success': False,
#                 'data': serializer.errors,
#                 }, status=status.HTTP_404_NOT_FOUND)


class QuizViewDetail(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class OptionView(APIView):
    '''
    this is the view for the options of a question'''
    serializer_class = OptionSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            option = Option.objects.create(**validated_data)
            serializer = OptionSerializer(option)
            return Response({
                'success': True,
                'message': 'Option logged successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request):
    '''Returns the questions conforming to the quiz
    '''
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            for key, value in data.items():
                option = Option.objects.get(pk=value)
                question = Question.objects.get(pk=option.question_id)
                question_answered = Question.objects.get(pk=key)
                if question == question_answered:
                    answers = Answer.objects.create(
                        user=user,
                        question=question,
                        option=option
                    )
                print(answers)

            return JsonResponse({'message': 'Quiz submitted successfully!'})
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
        except Option.DoesNotExist:
            return JsonResponse({'error': 'Option not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def calculate_scores(user, quiz):
    answers = Answer.objects.filter(user=user, question__quiz=quiz)
    correct_answers = answers.filter(option__is_correct=True).count()
    print(correct_answers)
    total_questions = quiz.question_set.count()
    print(total_questions)
    score = (correct_answers / total_questions) * 100
    return score


# send user's result
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_result(request, quiz_id):
    try:
        user = request.user
        quiz = Quiz.objects.get(id=quiz_id)
        score = calculate_scores(user, quiz)
        Score.create_or_update_score(user=user, quiz=quiz, score=score)
        user.scores += score
        return JsonResponse({'score': score})
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)


def leaderboard(request):
    users = CustomUser.objects.all().order_by('-scores')
    return Response({
        'data': users
    })


def view_corrections(request, quiz_id):
    user = request.user
    answers = Answer.objects.filter(user=user, question__quiz=quiz_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    score = Score.objects.get(user=user, quiz=quiz)
    for answer in answers:
        answer.correct_options = answer.question.options.filter(is_correct=True)
    return render(request, 'Authentication/view_corrections.html', {
        'answers': answers,
        'quiz': quiz,
        'score': score})

# administration views


def create_question(request):
    levels = Level.objects.all()
    quizes = Quiz.objects.all()
    if request.method == "POST":
        # print(request.POST)
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1_text')
        option2 = request.POST.get('option2_text')
        option3 = request.POST.get('option3_text')
        option4 = request.POST.get('option4_text')
        correct_option = request.POST.get('correct_option')
        level = request.POST.get('level')
        quiz = request.POST.get('quiz')
        question_level = Level.objects.get(pk=level)

        if Question.objects.filter(question_text=question_text, quiz_id=quiz).exists():
            return JsonResponse({
                'status': False,
                'message': 'A question with this text already exists.'
            }, status=400)

        question = Question.objects.create(
            question_text=question_text,
            level=question_level,
            quiz=Quiz.objects.get(pk=quiz)
        )

        options = [
            Option.objects.create(question=question, text=option1,
                                  is_correct=(correct_option == 'option1')),
            Option.objects.create(question=question, text=option2,
                                  is_correct=(correct_option == 'option2')),
            Option.objects.create(question=question, text=option3,
                                  is_correct=(correct_option == 'option3')),
            Option.objects.create(question=question, text=option4,
                                  is_correct=(correct_option == 'option4'))
            ]
        serialized_data = QuestionSerializer(question)
        print(serialized_data.data)
        return JsonResponse({
                'status': True,
                'data': serialized_data.data,
                'message': 'Option logged successfully'
            }, status=201)
    return render(request, 'main/addQuestion.html', {'levels': levels, 'quizes': quizes})


def addQuiz(request):
    if request.method == "POST":
        data = {
            'title': request.POST.get('quiz_title'),
            'description': request.POST.get('quiz_descr')
        }
        serializer = QuizSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            quiz = Quiz.objects.create(**validated_data)
            serializer = QuizSerializer(quiz)
            return JsonResponse({
                'success': True,
                'data': serializer.data,
            }, status=201)
        return JsonResponse({
            'success': False,
            'data': serializer.errors,
        }, status=400)
    return render(request, 'main/addQuiz.html')
