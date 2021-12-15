from django.forms import ModelForm
from django import forms
from app.models import *


class ProviderCreateForm(ModelForm):
    name = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your name'
        }
    ))
    owner = forms.CharField(required = True,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Owner name'
        }
    ))
    
    email = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your address'
        }
    ))
    # password = forms.CharField(required = True,widget=forms.PasswordInput(
    #     attrs={
    #     'class':'form-control'
    #     }
    # ))

    tax_id = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Tax Id'
        }
    ))

    class Meta:
        model = Provider
        fields = ["name","owner","tax_id","email"]

