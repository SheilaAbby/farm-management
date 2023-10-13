from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    # Add additional fields as needed
    role = models.CharField(max_length=50)
