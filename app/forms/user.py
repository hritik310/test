from django.forms import IntegerField, ModelForm
from django import forms
from datetime import datetime
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

    #     def clean_date_(self):
    #         dob = self.cleaned_data['date_of_birth']
    #         age = (datetime.now() - dob).days/365
    #         if age < 18:
    #             raise forms.ValidationError('Must be at least 18 years old to register')
    #         return dob

    # def clean(self):
 
    #     super(AddCreateForm,self).clean()


    #     date_of_birth = self.cleaned_data.get('date_of_birth') 
       
    #     age = (datetime.now() - date_of_birth).days/365

    #     if age < 18:
    #         raise forms.ValidationError('Must be at least 18 years old to register')
    #     return date_of_birth