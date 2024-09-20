from typing import Iterable
from django.db import models
import datetime
from employee.models import Model_MNF_detail
from django.contrib.postgres.fields import ArrayField

def default_count():
    return {"Total": 0, "Approved": 0, "Waiting": 0}

def default_data():
    return {'DVT': [], 'PP': [], 'MP': []}

# Create your models here.
class AC(models.Model):
    ModelName = models.CharField(max_length=100,default='')
    BImotor = models.CharField(max_length=100,default='')
    Blower = models.CharField(max_length=100,default='')
    FanMotor = models.CharField(max_length=100,default='')
    Eva = models.CharField(max_length=100,default='')
    Fan = models.CharField(max_length=100,default='')
    ConPipe = models.CharField(max_length=100,default='')
    CondCoil = models.CharField(max_length=100,default='')
    RefCharge = models.CharField(max_length=100,default='')
    Capilary = models.CharField(max_length=100,default='')
    Compressor  = models.CharField(max_length=100,default='')
    def __str__(self):
        return f"AC - {self.ModelName}"

class WM_FATL(models.Model):
    ModelName = models.CharField(max_length=100,default='')
    Type =  models.CharField(max_length=100,default='Fully Automatic Top Load Washing Machine')
    RatedCapacity = models.CharField(max_length=100,default='')
    RatedPower = models.CharField(max_length=100,default='')
    RatedSupply = models.CharField(max_length=100,default='')
    RatedFrequency = models.CharField(max_length=100,default='')
    RatedRPM = models.CharField(max_length=100,default='')
    def __str__(self):
        return f"{self.ModelName} - {self.Type}"
    
class Phone(models.Model):
    ModelName = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.ModelName} "
    
class TV(models.Model):
    ModelName = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.ModelName} "

class Model_Test_Name_Details(models.Model):
    Model_Name = models.ForeignKey(Model_MNF_detail, to_field="Indkal_model_no", on_delete=models.CASCADE)
    Product = models.CharField(max_length=100, blank=True, null=True)
    Test_Names = models.JSONField(default=default_data)
    Test_Count = models.JSONField(default=default_data)
    Time_Line = models.JSONField(default=dict)
    def save(self, *args, **kwargs):
        if self.Model_Name:
            self.Product = self.Model_Name.Product
        if self.Test_Names:
            self.Test_Count = {key: len(val) for key, val in self.Test_Names.items()}
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.Product} - {self.Model_Name}"
    
class Product_List(models.Model):
    Product = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.Product}"
    
class Summary(models.Model):
    Model_Name = models.ForeignKey(Model_MNF_detail, to_field="Indkal_model_no", on_delete=models.CASCADE)
    Product = models.CharField(max_length=100, blank=True, null=True)
    Model_Details = models.JSONField(default=dict)
    Dates = models.JSONField(default=default_data)
    Status = models.JSONField(default=default_data)
    PT = models.JSONField(default=default_count)
    LT = models.JSONField(default=default_count)
    BT = models.JSONField(default=default_count)
    def save(self, *args, **kwargs):
        if self.Model_Name:
            self.Product = self.Model_Name.Product
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.Model_Name}"