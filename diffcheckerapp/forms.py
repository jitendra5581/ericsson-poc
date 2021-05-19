from django.forms import ModelForm, PasswordInput
from .models import *
from django import forms

class DeviceForm(ModelForm):
    password = forms.CharField(widget=PasswordInput())
    secret = forms.CharField(widget=PasswordInput())

class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File")
