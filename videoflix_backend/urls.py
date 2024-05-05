"""
URL configuration for videoflix_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from users.views import register_api, verify_email, login_api, send_password_reset, set_new_password, LogoutAPIView
from content import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('register/', register_api, name='register_api'),
    path('verify-email/', verify_email, name='verify_email'),
    path('login', login_api, name='login_api'),
    path('password-reset', send_password_reset, name='send_password_reset'),
    path('set-password', set_new_password, name='set_new_password'),
     path('videos/<str:title>/480p/', views.stream_video_480p, name='stream_video_480p'),
    path('videos/<str:title>/720p/', views.stream_video_720p, name='stream_video_720p'),
    path('videos', views.movie_list, name='movie_list' ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView, name='logout'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)