from django import forms
from .models import *
from django.forms import formset_factory
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from ckeditor5.fields import RichTextFormField


class TestRecordForm(forms.ModelForm):
    class Meta:
        model = TestRecord
        fields = ['test_date','result','sample_quantiy']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
          
            # 'result': RichTextFormField()
        }

testItemFormset = formset_factory(TestRecordForm, extra=1)
