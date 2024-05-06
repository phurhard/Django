from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny)


from Authentication.models import Answer, Option, Question, Quiz, QuizSet, Score
# from .models import CustomUser as User
from .serializers import (
    AnswerSerializer,
    QuestionSerializer,
    QuizSerializer,
    QuizSetSerializer,
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
    permission_classes = [IsAdminUser]

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


class QuizSetView(APIView):
    '''
    Only an admin account can create a quiz'''
    serializer_class = QuizSetSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        '''
        This creates a new quiz'''
        serializer = QuizSetSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            quiz = QuizSet.objects.create(**validated_data)
            serializer = QuizSetSerializer(quiz)
            return Response({
                'success': True,
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'data': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self):
        '''
        Returns all the quizsets'''
        try:
            quizes = QuizSet.objects.all()
            serializer = QuizSetSerializer(quizes, many=True)
            return Response({
                'succes': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'success': False,
                'message': serializer.errors
            }, status=status.HTTP_409_CONFLICT)


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
