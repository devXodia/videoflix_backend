from django.shortcuts import render
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .utility import generate_verification_token
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

CACHETTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# @cache_page(CACHETTL)

User = get_user_model()



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
            verification_link = f'https://localhost:4200/verify/{verification_token}'

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