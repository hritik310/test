from django.forms import ModelForm
from django import forms
from app.models import *

class ShipperCreateForm(ModelForm):
	itn = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Internal Transaction Number'
        }  
    ))
	date = forms.DateField(required = True,widget=forms.DateInput(
        attrs={
        'class':'form-control',
        'type': 'date',
        'placeholder':'Select date'
        }
    ))

	refrence = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Reference'
        }  
    ))
	name = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Your name'
        }
    ))
	vin = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Vehicle Identification Number'
        }
    ))

	make = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Make name'
        }
    ))
	year = forms.IntegerField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Year'
        }
    ))
	note = forms.CharField(required = False,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Write Youe Note Here.'
        }
    ))

	class Meta:
		model = Shipper_Exports
		fields = ["itn","date","refrence","name","vin","make","year","note"]
