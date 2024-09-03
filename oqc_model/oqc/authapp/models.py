from django.db import models
from datetime import datetime as dt
from product.models import Product_Test_Name_Details
from django.contrib.postgres.fields import ArrayField

def product_choice():
    return {k: False for k in Product_Test_Name_Details.objects.values_list('Product', flat=True)}

# Create your models here.
class Employee(models.Model):
    user_type = models.CharField(max_length=50, null=True, choices=[("employee", "Employee"), ("owner", "Owner"), ("legal", "Legal"), ("brand", "Brand")], blank=True)
    product_type = models.JSONField(default=product_choice)
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
    def __str__(self):
        return f"{self.user} {self.otp}"
    
def default_notification():
    return {"action": "", "display_content": "", "display_full_content": "","created_at": dt.now().strftime("%Y-%m-%d %H:%M:%S"), "metadata": {"product": "", "model": "", "stage": "", "test": ""}, "is_read": False, "is_cleared": False}

class Notification(models.Model):
    employee = models.ForeignKey(Employee, to_field="username", on_delete=models.CASCADE)
    notification = ArrayField(models.JSONField(default=default_notification), default=list)
    unread_count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.employee.username}"