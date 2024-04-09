from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    custom = models.JSONField(null=True)
    phone = models.CharField(max_length = 500, default='')
    address = models.CharField(max_length = 500, default='')
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    
    objects = CustomUserManager()
