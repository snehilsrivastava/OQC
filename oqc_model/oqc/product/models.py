from django.db import models
import datetime

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

    
    

class Washing_Machine(models.Model):
    no = models.IntegerField()
    ModelName = models.CharField(max_length=100)
    Date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.no} - {self.Date} - {self.ModelName} "
    
class Phone(models.Model):
    no = models.IntegerField()
    ModelName = models.CharField(max_length=100)
    Date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.no} - {self.Date} - {self.ModelName} "
    
class TV(models.Model):
    no = models.IntegerField()
    ModelName = models.CharField(max_length=100)
    Date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.no} - {self.Date} - {self.ModelName} "
    
class Product_Detail(models.Model):
    no = models.IntegerField()
    ProductType = models.CharField(max_length=100)
    ModelName = models.CharField(max_length=100)
    SerailNo = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.no}- {self.ProductType} - {self.SerailNo} - {self.ModelName} "
     



    
    
    
