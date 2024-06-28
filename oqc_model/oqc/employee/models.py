from django.db import models
from authapp.models import Employee
import datetime
from product.models import  Product_Detail
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.

class Test(models.Model):
    no = models.IntegerField()  # Corrected: Added parentheses
    start_date = models.DateField(auto_now=False, auto_now_add=False)  # Removed empty string
    end_date = models.DateField(auto_now=False, auto_now_add=False)  # Removed empty string

    def __str__(self):
        return f"Test {self.no} from {self.start_date} to {self.end_date}"
    
class Model_MNF_detail(models.Model):

    Customer = models.CharField(max_length=500,default='None')
    Manufature = models.CharField(max_length=500,default='None')
    Location = models.CharField(max_length=100,default='None')
    Brand = models.CharField(max_length=80,default='None')
    Product = models.CharField(max_length=80,default='None')
    Brand_model_no = models.CharField(max_length=80,default='None')
    Indkal_model_no = models.CharField(max_length=80,default='None')
    ORM_model_no = models.CharField(max_length=80,default='None')
    def __str__(self):
        return f"{self.Product} - {self.Indkal_model_no}"



class Test_core_detail(models.Model):
  
    TestName =  models.CharField(max_length=500,default='None')
    Test_Objective = models.CharField(max_length=500,default='None')
    Test_Standard = models.CharField(max_length=500,default='None')
    Test_Condition = models.TextField(max_length=500,default='None')
    Test_Procedure = models.TextField(max_length=500,default='None')
    Judgement = models.TextField(max_length=500,default='None')
    Instrument = models.CharField(max_length=500,default='None')
    def __str__(self):
        return f"{self.TestName}"

class TestStageDetail(models.Model):
    ModelName = models.CharField(max_length=80,default='None')
    TestStage = models.CharField(max_length=20,default='None')
    Test_Report_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.ModelName}"

    
class TestRecord(models.Model):
    employee = models.CharField(max_length=80, default = 'None')
    test_date = models.DateField(default=datetime.date.today)
    test_start_date = models.DateField(default=datetime.date.today)
    test_end_date = models.DateField(default=datetime.date.today)
    sample_quantiy = models.IntegerField(default=0)
    result = RichTextUploadingField(default="None", blank=True)
    notes = models.CharField(max_length=255, default="None") 
    employee_remark  = models.TextField(max_length=500,default="None")
    owner_remark  = models.TextField(max_length=500,default="None")
    status = models.BooleanField(default = False)
    ProductType = models.CharField(max_length=102,default = "None")
    ModelName = models.CharField(max_length=100,default = "None")
    SerailNo  = models.CharField(max_length=100,default = "None")
    TestStage = models.CharField(max_length=20,default="None")
    TestName  = models.CharField(max_length=80,default="None")
    # mnfDetail = models.ForeignKey(ModelMNFdetail,on_delete= models.CASCADE,related_name = 'test_mnf_detail')

    def __str__(self):
        return f"{self.SerailNo}"
    
class TestImage(models.Model):
    report = models.ForeignKey(TestRecord, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="test_images/", height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f"Image for {self.report.test_name}"
    

class TestList(models.Model):
    TestStage = models.CharField(max_length=20,default='None')
    Product = models.CharField(max_length=35,default='None')
    TestName = models.CharField(max_length=80,default='None')

    def __str__(self):
     return f"{self.Product} - {self.TestName}"
