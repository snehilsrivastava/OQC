from django import forms
from .models import TestRecord,TestImage
from django.forms import formset_factory


class TestRecordForm(forms.ModelForm):
    class Meta:
        model = TestRecord
       
        fields = ['test_date','result','sample_quantiy', 'test_start_date', 'test_end_date']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'test_start_date': forms.DateInput(attrs={'type': 'date'}),
            'test_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

testItemFormset = formset_factory(TestRecordForm, extra=1)


class TestImageForm(forms.ModelForm):
    class Meta:
        model = TestImage
        fields = ['image']

