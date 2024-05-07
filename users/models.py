from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    custom = models.JSONField(null=True)
    phone = models.CharField(max_length=500, default='')
    address = models.CharField(max_length=500, default='')
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    first_name = models.CharField(default='', max_length=20)
    last_name = models.CharField(default='', max_length=20)
    username = models.CharField(null=True, max_length=30, unique=True)
    verification_token = models.CharField(max_length=50, default='')
    password_reset_token = models.CharField(max_length=50, default='')
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email