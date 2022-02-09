from django.forms import IntegerField, ModelForm
from django import forms

from vote.models import *

class AddCreateForm(ModelForm):
    email = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your Email address'
        }
    ))
    name = forms.CharField(label="Legal_name",required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your name',
        
        }
    ))
 
    password = forms.CharField(required = True,widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your Password',
        }
    ))


    address=forms.CharField(required=True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your address'
        
        }
    ))


    class Meta:
        model = user
        fields = ["name","email","address","password"]