from django.forms import IntegerField, ModelForm
from django import forms

from app.models import *

class AddCreateForm(ModelForm):
    email = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your Email address'
        }
    ))
    username = forms.CharField(label="Username",required = True,widget=forms.TextInput(
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

    first_name= forms.CharField(label="Firstname",required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your Firstname',
        
        }
    ))

    last_name = forms.CharField(label="Lastname",required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your Lastname',
        
        }
    ))
  
    phone_number=forms.IntegerField(label="Phone number")

    date_of_birth=forms.DateField(label="Date of Birth",required = True,widget=forms.DateInput(
        attrs={
        'class':'form-control',
        'type': 'date',
        'placeholder':'Select date'
        }
    ))

    class Meta:
        model = user
        fields = ["first_name","last_name","email","username","password","phone_number","date_of_birth"]