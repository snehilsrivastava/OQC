from django.db import models

# Create your models here.
class Employee(models.Model):
    user_type = models.CharField(max_length=50, null=True, choices=[("employee", "Employee"), ("owner", "Owner"), ("legal", "Legal"), ("brand", "Brand")], blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username  = models.CharField(max_length=255, unique=True)
    password =  models.CharField(max_length=255)
    last_login = models.TimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username}"

class OTP(models.Model):
    user = models.CharField(max_length=255)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)