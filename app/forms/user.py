from django.forms import IntegerField, ModelForm
from django import forms
from datetime import datetime
from app.models import *
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from datetime import date
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


FRUIT_CHOICES= [
    ('I agree with Privacy Policy and Terms & Conditions of the website.','I agree with Privacy Policy and Terms & Conditions of the website.'),
    
]

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


    terms_and_conditions= forms.BooleanField(widget=forms.CheckboxSelectMultiple(choices=FRUIT_CHOICES))

    password=forms.CharField(widget=forms.PasswordInput( attrs={
         'class':'form-control',
         'placeholder':'Enter your Password',
        }),validators=[validate_password])
    # password = forms.CharField(required = True,widget=forms.PasswordInput(
    #     attrs={
    #     'class':'form-control',
    #     'placeholder':'Enter your Password',
    #     }
    # ))

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
  
    phone_number=forms.IntegerField(label="Phone Number",required = True,widget=forms.TextInput(
        attrs={
        'max_length':10,
        'class':'form-control',
        'placeholder':'Enter Phone number',
        'type':'number'
        
        }

    ))

    date_of_birth=forms.DateField(label="Date of Birth",required = True,widget=forms.DateInput(
        attrs={
        'class':'form-control',
        'type': 'date',
        'placeholder':'Select date'
        }
    ))

    # address=forms.CharField(label="Address",required = True,widget=forms.TextInput(
    #     attrs={
    #     'class':'form-control',
    #     'placeholder':'Enter your address',
        
    #     }
    # ))

    # zip=forms.IntegerField(label="Zip",required = True,widget=forms.TextInput(
    #     attrs={
    #     'class':'form-control',
    #     'placeholder':'Enter Zip',
    #     'type':'number'
    #     }
    # ))
    # title=forms.CharField(label="Title",required = True,widget=forms.TextInput(
    #     attrs={
    #     'class':'form-control',
    #     'placeholder':'Enter your title',
        
        
    #     }
    # ))


    class Meta:
        model = user
        fields = ["username","last_name","email","password","phone_number","date_of_birth","first_name","terms_and_conditions"]

    #     def clean_date_(self):
    #         dob = self.cleaned_data['date_of_birth']
    #         age = (datetime.now() - dob).days/365
    #         if age < 18:
    #             raise forms.ValidationError('Must be at least 18 years old to register')
    #         return dob

    # def clean(self):
 
    #     super(AddCreateForm,self).clean()


    #     password = self.cleaned_data.get('password') 

    #     if len(password) < 8:
    #         raise forms.ValidationError('length of password must be  atleast 9 ')
    #     return password

    def clean(self):
          cleaned_data=super(AddCreateForm, self).clean()
          date_of_birth = cleaned_data.get('date_of_birth')
          phone_number= cleaned_data.get('phone_number')
          age = (date.today() - date_of_birth).days / 365
          print("age",age)
          if age < 18:
            self.add_error("date_of_birth", forms.ValidationError("Age must be above 18") 
          )
    
          ph_num=str(phone_number)
          print(ph_num)#dflklg
          if len(ph_num)>15 or len(ph_num)<10:
            print("dfs")
            self.add_error("phone_number", forms.ValidationError("Phone number must be of 10 digit")
            )
    #     # def clean(self):
    #     # cleaned_data = super(AddCreateForm, self).clean()
    #     # password = cleaned_data.get("password")
    #     # confirm_password = cleaned_data.get("confirmation")

    #     # if password != confirm_password:
    #     #      self.add_error("confirmation", forms.ValidationError("password and confirm_password does not match") 
    #     #     # raise forms.ValidationError(
    #     #     #     "password and confirm_password does not match"
    #     #     )  