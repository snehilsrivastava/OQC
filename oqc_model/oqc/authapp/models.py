from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
 user_type = models.CharField(max_length=50)
 username  = models.CharField(max_length=255)
 password =  models.CharField(max_length=255)
 def __str__(self):
        return f"{self.username} "




