from django import forms
from .models import *
from django.forms import formset_factory
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from ckeditor5.fields import RichTextFormField


class TestRecordForm(forms.ModelForm):
    class Meta:
        model = TestRecord
        fields = ['test_date','result','sample_quantiy', 'test_start_date', 'test_end_date', 'additional_details']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'test_start_date': forms.DateInput(attrs={'type': 'date'}),
            'test_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

testItemFormset = formset_factory(TestRecordForm, extra=1)
