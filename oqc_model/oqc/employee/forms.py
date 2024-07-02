from django import forms
from .models import *
from django.forms import formset_factory
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from ckeditor5.fields import RichTextFormField


class TestRecordForm(forms.ModelForm):
    class Meta:
        model = TestRecord
        fields = ['test_date','result','sample_quantiy', 'test_start_date', 'test_end_date']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'test_start_date': forms.DateInput(attrs={'type': 'date'}),
            'test_end_date': forms.DateInput(attrs={'type': 'date'}),
            # 'result': RichTextFormField()
        }

testItemFormset = formset_factory(TestRecordForm, extra=1)

# class TestRemarkForm(forms.ModelForm):
#     class Meta:
#         model = TestRecord
       
#         fields = ['employee_remark','owner_remark']
       
# testRemarkFormset = formset_factory(TestRemarkForm, extra=1)

class TestImageForm(forms.ModelForm):
    class Meta:
        model = TestImage
        fields = ['image']
