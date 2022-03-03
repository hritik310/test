from django.forms import IntegerField, ModelForm
from django import forms
from datetime import datetime
from app.models import *
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from datetime import date
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError



class userform(ModelForm):
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

    phone_number=forms.IntegerField(label="Phone Number",required = True,widget=forms.TextInput(
        attrs={
        'max_length':10,
        'class':'form-control',
        'placeholder':'Enter Phone number',
        'type':'number'
        
        }

    ))

    class Meta:
        model = user
        fields = ["username","email","phone_number"]


    
    def clean(self):
          cleaned_data=super(userform, self).clean()   
      
          phone_number= cleaned_data.get('phone_number')
          ph_num=str(phone_number)
          print(ph_num)#dflklg
          if len(ph_num)>15 or len(ph_num)<10:
            print("dfs")
            self.add_error("phone_number", forms.ValidationError("Phone number must be between 10 and 15 digit")
            )    