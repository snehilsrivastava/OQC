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