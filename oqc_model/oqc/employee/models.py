from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField

# Create your models here.
    
class Model_MNF_detail(models.Model):
    Customer = models.CharField(max_length=500,default='None')
    Manufacture = models.CharField(max_length=500,default='None')
    Location = models.CharField(max_length=100,default='None')
    Brand = models.CharField(max_length=80,default='None')
    Product = models.CharField(max_length=80,default='None')
    Brand_model_no = models.CharField(max_length=80,default='None')
    Indkal_model_no = models.CharField(max_length=80,default='None', unique=True)
    ODM_model_no = models.CharField(max_length=80,default='None')
    def __str__(self):
        return f"{self.Product} - {self.Indkal_model_no}"

class Test_core_detail(models.Model):
    ProductType = models.CharField(max_length=500,default='None')
    TestName =  models.CharField(max_length=500,default='')
    TestStage = models.CharField(max_length=20,default='')
    Test_Objective = models.CharField(max_length=500,default='')
    Test_Standard = models.CharField(max_length=500,default='')
    Test_Condition = models.TextField(max_length=500,default='')
    Test_Procedure = models.TextField(max_length=700,default='')
    Judgement = models.TextField(max_length=500,default='')
    Instrument = models.CharField(max_length=500,default='')
    def __str__(self):
        return f"{self.ProductType} | {self.TestName}"
    
class TestRecord(models.Model):
    test_date = models.DateField(default=datetime.date.today)
    test_start_date = models.DateField(default=datetime.date.today)
    test_end_date = models.DateField(default=datetime.date.today)
    verification = models.BooleanField(default=False)
    sample_quantiy = models.IntegerField(default=0)
    result = RichTextUploadingField(default="", blank=True)
    additional_details = ArrayField(RichTextUploadingField(default="", blank=True), default=list, blank=True)
    remarks = models.TextField(default=str, blank=True)
    status = models.CharField(max_length=50,default="Not Sent")
    L_status = models.CharField(max_length=50,default="Not Sent")
    B_status = models.CharField(max_length=50,default="Not Sent")
    ProductType = models.CharField(max_length=102,default = "None")
    ModelName = models.CharField(max_length=100,default = "None")
    SerailNo  = models.CharField(max_length=100,default = "None")
    TestStage = models.CharField(max_length=20,default="None")
    TestName  = models.CharField(max_length=80,default="None")
    owner_name = models.CharField(max_length=80, default = 'None')
    html_content = models.TextField(default="")
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    def __str__(self):
        return f"{self.ProductType} - {self.ModelName} - {self.TestName}"