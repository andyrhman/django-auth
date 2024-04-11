from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    # remove the default username field in django AbstractUser
    username = None 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
