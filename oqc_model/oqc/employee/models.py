from django.db import models
from authapp.models import Employee
import datetime
from product.models import  Product_Detail
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.
    
class Model_MNF_detail(models.Model):

    Customer = models.CharField(max_length=500,default='None')
    Manufacture = models.CharField(max_length=500,default='None')
    Location = models.CharField(max_length=100,default='None')
    Brand = models.CharField(max_length=80,default='None')
    Product = models.CharField(max_length=80,default='None')
    Brand_model_no = models.CharField(max_length=80,default='None')
    Indkal_model_no = models.CharField(max_length=80,default='None')
    ODM_model_no = models.CharField(max_length=80,default='None')
    def __str__(self):
        return f"{self.Product} - {self.Indkal_model_no}"



class Test_core_detail(models.Model):
    ProductType = models.CharField(max_length=500,default='None')
    TestName =  models.CharField(max_length=500,default='None')
    Test_Objective = models.CharField(max_length=500,default='None')
    Test_Standard = models.CharField(max_length=500,default='None')
    Test_Condition = models.TextField(max_length=500,default='None')
    Test_Procedure = models.TextField(max_length=500,default='None')
    Judgement = models.TextField(max_length=500,default='None')
    Instrument = models.CharField(max_length=500,default='None')
    def __str__(self):
        return f"{self.TestName}"
    
class TestRecord(models.Model):
    employee = models.CharField(max_length=80, default = 'None')
    employee_name = models.CharField(max_length=80, default = 'None')
    test_date = models.DateField(default=datetime.date.today)
    test_start_date = models.DateField(default=datetime.date.today)
    test_end_date = models.DateField(default=datetime.date.today)
    verification = models.BooleanField(default=False)
    sample_quantiy = models.IntegerField(default=0)
    result = RichTextUploadingField(default="", blank=True)
    additional_details = RichTextUploadingField(default="", blank=True, config_name='full')
    notes = models.CharField(max_length=255, blank=True) 
    employee_remark  = models.TextField(max_length=500,default='',blank=True)
    owner_remark  = models.TextField(max_length=500,default='',blank=True)
    status = models.CharField(max_length=50,default="Not Sent")
    L_status = models.CharField(max_length=50,default="Not Sent")
    B_status = models.CharField(max_length=50,default="Not Sent")
    ProductType = models.CharField(max_length=102,default = "None")
    ModelName = models.CharField(max_length=100,default = "None")
    SerailNo  = models.CharField(max_length=100,default = "None")
    TestStage = models.CharField(max_length=20,default="None")
    TestName  = models.CharField(max_length=80,default="None")
    owner_name = models.CharField(max_length=80, default = 'None')

    def __str__(self):
        return f"{self.SerailNo}"


class TestList(models.Model):
    TestStage = models.CharField(max_length=20,default='None')
    Product = models.CharField(max_length=35,default='None')
    TestName = models.CharField(max_length=80,default='None')

    def __str__(self):
     return f"{self.Product} - {self.TestName}"
