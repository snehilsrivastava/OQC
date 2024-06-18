from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget

class TestRecordForm(forms.ModelForm):
    class Meta:
        model = TestRecord
        fields = ['test_name', 'test_date', 'result', 'notes']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TestImageForm(forms.ModelForm):
    class Meta:
        model = TestImage
        fields = ['image']

class RTF_Form(forms.ModelForm):
    class Meta:
        model = RTF_Test
        fields = '__all__'
