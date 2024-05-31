from rest_framework import status
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser as User, Score, Quiz
from .serializers import (
    ProfileSerializer,
    UserLoginSerializer,
    UserSerializer,
    TokenRefreshSerializer
    )
from main.serializers import (
    ScoreSerializer,
    QuizSerializer)

# Create your views here.


class UserSignup(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                age=validated_data.get('age')
            )
            return Response({
                'success': True,
                'message': 'User created successfully',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'Authentication/register.html')


class AdminSignup(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            User.objects.create_superuser(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                age=validated_data.get('age')
            )
            return Response({
                'success': True,
                'message': 'Superuser created successfully',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'Authentication/register.html')


class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            email = validated_data.get('email')
            password = validated_data.get('password')

            # user = User.objects.filter(email=email).first()
            user = authenticate(request, email=email, password=password)
            if user is None:
                return Response({
                    'success': False,
                    'message': 'No user found with that username'
                    },
                    status=status.HTTP_404_NOT_FOUND
                    )
            if not user.check_password(password):
                return Response({
                    'success': False,
                    'message': 'Invalid password provided'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                    )
            login(request, user)
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                'success': True,
                'message': 'Logged in Successfully',
                'data': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Logged in unsuccessful',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'Authentication/login.html')


class RefreshTokenView(TokenViewBase):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh')
        access_token = RefreshToken(refresh_token).access_token
        return Response({'access': str(access_token)})


@login_required
def profile_view(request):
    '''
    This renders the profile page'''
    user = request.user
    scores = Score.objects.filter(user=user.id)
    serializer = ScoreSerializer(scores, many=True)
    return render(request, 'Authentication/profile.html',
                  {'scores': serializer.data})


@login_required
def home_view(request):
    '''
    This renders the home page'''
    users = User.objects.all()
    top_users = users.order_by('-scores')[:3]
    serializer = ProfileSerializer(top_users, many=True)
    leaderboard = users.order_by('-scores')
    leaderboard_serializer = ProfileSerializer(leaderboard, many=True)
    return render(request, 'Authentication/home.html',
                  {'top_users': serializer.data, 'leaderboard': leaderboard_serializer.data})


@login_required
def quiz_view(request):
    '''
    This renders the quiz page'''
    # gets all the quiz objs
    user = request.user
    user_scores = Score.objects.filter(user=user)
    quizes_taken = Quiz.objects.filter(score__in=user_scores)
    quizserializer = QuizSerializer(quizes_taken, many=True)
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return render(request, 'Authentication/quiz.html',
                  {'quizes': serializer.data,
                   'quizes_taken': quizserializer.data})


def logout_view(request):
    '''Logs out the user'''
    logout(request)
    return redirect('login')
