from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
class User(AbstractUser):
    # ? https://stackoverflow.com/questions/61464113/django-db-utils-programmingerror-cannot-cast-type-uuid-to-integer
    """
    1) add temp_id = models.UUIDField(default=uuid.uuid4) to your model, then run makemigrations

    2) * add primary_key=True to the temp_id field, then run makemigrations again
    
    3) * add editable=False to the temp_id field, then run makemigrations again

    4) rename the field to id (or to whatever you want), then run makemigrations a third time

    5) push the migrations to the database via python manage.py migrate
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    tfa_secret = models.CharField(max_length=255, default='')

    # remove the default username field in django AbstractUser
    username = None 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserToken(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=False, editable=False)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    
class Reset(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    used = models.BooleanField(default=False)