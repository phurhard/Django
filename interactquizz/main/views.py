from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny)


from Authentication.models import Answer, Question, Score
# from .models import CustomUser as User
from .serializers import (
    AnswerSerializer,
    QuestionSerializer,
    ScoreSerializer,
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
