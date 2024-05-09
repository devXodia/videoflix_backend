
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from .serializers import UserRegistrationSerializer
from .utility import generate_verification_token, generate_password_reset_token
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



CACHETTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

""" @cache_page(CACHETTL) """

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error occurred while logging out."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def register_api(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate verification token (for demonstration purposes, you need to implement this)
            verification_token = generate_verification_token(user)

            user.verification_token = verification_token
            user.save()

            # Construct verification link
            verification_link = f'https://alen-alduk.developerakademie.org/verify/{verification_token}'

            # Send verification email
            subject = 'Welcome to Videoflix!'
            message = render_to_string('verification_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            user_email = user.email
            send_mail(subject, message, 'videoflix@alen-alduk.com', [user_email])

            # Return success response
            return Response({'message': 'User registered successfully. Please check your email for verification.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_email(request):
    if request.method == 'POST':
        token = request.data.get('token')
        if token:
            user = User.objects.filter(verification_token=token).first()
            if user:
                user.email_verified = True
                user.save()
                # Return a success message
                return Response({'message': 'User verified.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.email_verified:
                # Generate JWT tokens
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Email not verified'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@api_view(['POST'])
def send_password_reset(request):
    if request.method == 'POST':
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token
        password_reset_token = generate_password_reset_token(user)

        # Save password reset token to user model
        user.password_reset_token = password_reset_token
        user.save()

        # Construct password reset link
        password_reset_link = f'https://alen-alduk.developerakademie.org/set-password/{password_reset_token}'

        # Send password reset email
        subject = 'Password Reset Request'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'password_reset_link': password_reset_link,
        })
        send_mail(subject, message, 'videoflix@alen-alduk.com', [email])

        # Return success response
        return Response({'message': 'Password reset instructions sent to your email.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def set_new_password(request):
    if request.method == 'POST':
        token = request.data.get('token')
        password = request.data.get('password')
        if token:
            user = User.objects.filter(password_reset_token=token).first()
            if user:
                user.set_password(password)
                user.save()
                # Return a success message
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)