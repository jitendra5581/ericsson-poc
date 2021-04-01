from django.forms import ModelForm, PasswordInput
from .models import *
from django import forms

class DeviceForm(ModelForm):
    password = forms.CharField(widget=PasswordInput())
    secret = forms.CharField(widget=PasswordInput())
