from rest_framework import status
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from .forms import ProfileImageUpload
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser as User, Score, Quiz, Level
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


def create_user(serializer, is_superuser=False):
    """
    Create a user or superuser based on the serializer data.

    Args:
        serializer (UserSerializer): The serializer containing user data.
        is_superuser (bool): Flag to determine if the user is a superuser.

    Returns:
        tuple: A tuple containing the user object and any errors encountered.
    """
    if serializer.is_valid():
        validated_data = serializer.validated_data
        if is_superuser:
            user = User.objects.create_superuser(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data.get('last_name'),
                age=validated_data.get('age')
            )
        else:
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data.get('last_name'),
                age=validated_data.get('age')
            )
        return user, None
    return None, serializer.errors

class UserSignup(APIView):
    """
    API view for user signup.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user, errors = create_user(serializer)
        if user:
            return Response({
                'success': True,
                'message': 'User created successfully',
                'data': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Invalid credentials',
            'data': errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        return render(request, 'Authentication/register.html')


class AdminSignup(APIView):
    """
    API view for admin signup.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user, errors = create_user(serializer, is_superuser=True)
        if user:
            return Response({
                'success': True,
                'message': 'Superuser created successfully',
                'data': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'data': errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'Authentication/registerAdmin.html')


class UserLogin(APIView):
    """
    API view for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                validated_data = serializer. validated_data

                email = validated_data.get('email')
                password = validated_data.get('password')
                user = authenticate(request, email=email, password=password)
                if user is None:
                    return Response({
                        'success': False,
                        'message': 'Email is incorrect'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
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
                    'access': str(refresh.  access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Logging in unsuccessful',
                    'errors': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                    'success': False,
                    'message': 'Logging in unsuccessful',
                    'Reason': str(e),
                    'errors': serializer.errors,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return render(request, 'Authentication/login.html')


class RefreshTokenView(TokenViewBase):
    """
    API view for refreshing JWT tokens.
    """

    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh')
        access_token = RefreshToken(refresh_token).access_token
        return Response({
                    'success': True,
                    'message': 'Access token refreshed',
                    'data': str(access_token),
                }, status=status.HTTP_200_OK)


def landing_page(request):
    """
    Render the landing page.
    """
    return render(request, 'Authentication/landing_page.html')


@login_required
def profile_view(request):
    """
    Render the profile page for the logged-in user.

    Handles profile image upload and displays user scores.
    """
    user = request.user
    scores = Score.objects.filter(user=user)
    serializer = ScoreSerializer(scores, many=True)

    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile_image = request.FILES['profile_image']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(profile_image.name, profile_image)
        # uploaded_file_url = fs.url(filename)
        user.profile_image = filename
        user.save()
        return redirect('profile')
    else:
        form = ProfileImageUpload(instance=user)

    return render(request, 'Authentication/profile.html', {
        'scores': serializer.data,
        'user': user,
        'form': form
        })


@login_required
def home_view(request):
    """
    Render the home page with top users and leaderboard.

    Displays top users and leaderboard based on total scores.
    """
    users = User.objects.annotate(total_score=Coalesce(Sum('score__score'), 0))
    top_users = users.order_by('-total_score')[:3]
    top_users_serializer = ProfileSerializer(top_users, many=True)
    leaderboard = users.order_by('-total_score')
    leaderboard_serializer = ProfileSerializer(leaderboard, many=True)
    context = {
        'top_users': top_users_serializer.data,
        'leaderboard': leaderboard_serializer.data
        }
    return render(request, 'Authentication/home.html', context)


@login_required
def quiz_view(request):
    """
    Render the quiz page for the logged-in user.

    Displays available quizzes based on the user's level.
    """
    user = request.user
    user_scores = Score.objects.filter(user=user)
    user_level = user.level
    quizes_taken = Quiz.objects.filter(score__in=user_scores)
    quizserializer = QuizSerializer(quizes_taken, many=True)
    quizzes = Quiz.objects.annotate(
        num_questions=Count('question')
        ).filter(
            num_questions__gt=0,
            question__level=user_level,
            level=user_level
            ).distinct()
    serializer = QuizSerializer(quizzes, many=True)
    return render(request, 'Authentication/quiz.html',
                  {'quizes': serializer.data,
                   'quizes_taken': quizserializer.data})


@login_required
def logout_view(request):
    """
    Log out the current user and redirect to the login page.
    """
    logout(request)
    return redirect('login')
