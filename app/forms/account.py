from django.forms import ModelForm
from django import forms
from app.models import *


class AddCreateForm(ModelForm):
    username = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your name'
        }
    ))
    
    email = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your address'
        }
    ))
    password = forms.CharField(required = True,widget=forms.PasswordInput(
        attrs={
        'class':'form-control'
        }
    ))

    phone = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your phone number'
        }
    ))

    class Meta:
        model = User
        fields = ["username","phone","email","password"]