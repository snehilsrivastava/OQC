from django import forms
from .models import TestRecord,TestImage

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
