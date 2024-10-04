from django import forms
from .models import *
from django.forms import formset_factory
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from ckeditor5.fields import RichTextFormField


class TestRecordForm(forms.ModelForm):
    class Meta:
        model = TestRecord
        fields = ['result', 'sample_quantiy', 'SerailNo']
        widgets = {
            # 'test_date': forms.DateInput(attrs={'type': 'date'}),
        }

testItemFormset = formset_factory(TestRecordForm, extra=1)
