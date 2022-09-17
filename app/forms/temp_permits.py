from django.forms import ModelForm
from django import forms
from app.models import *


class Temp_PermitCreateForm(ModelForm):
	date = forms.DateField(required = True,widget=forms.DateInput(
        attrs={
        'class':'form-control',
        'type': 'date',
        'placeholder':'Select date'
        }
    ))
	name = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Your name'
        }
    ))
	VIEWS = (
		('', 'Select here.'),
        ('72', '72'),
        ('144', '144'),
    )
	hour = forms.ChoiceField(required = True,choices=VIEWS,widget=forms.Select(
        attrs={
        'class':'form-control'
        }
    ))

	permit_number = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Your Permit Number'
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
	note = forms.CharField(required = False,widget=forms.Textarea(
        attrs={
        'rows':4, 'cols':15,
        'class':'form-control',
        'placeholder':'Write Youe Note Here.'
        }
    ))


	class Meta:
		model = Temporary_Permits
		fields = ["date","name","hour","permit_number","vin","make","year","note"]