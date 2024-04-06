from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    custom = models.CharField(max_length = 500, default='')
    phone = models.CharField(max_length = 500, default='')
    adress = models.CharField(max_length = 500, default='')