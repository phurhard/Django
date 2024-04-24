from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.permissions import AllowAny
from .models import CustomUser as User
from .serializers import UserLoginSerializer, UserSerializer, TokenRefreshSerializer

# Create your views here.


class UserSignup(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'User created successfully',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({
                'success': False,
                'error': 'No user found with that username'
                },
                status=status.HTTP_401_UNAUTHORIZED
                )
        if not user.check_password(password):
            return Response({
                'success': False,
                'error': 'Invalid password'
                },
                status=status.HTTP_401_UNAUTHORIZED
                )
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Logged in Successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class RefreshTokenView(TokenViewBase):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh')
        access_token = RefreshToken(refresh_token).access_token
        return Response({'access': str(access_token)})
