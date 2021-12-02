from django.forms import ModelForm
from django import forms
from app.models import *
 
# define the class of a form
class AgencyCreateForm(ModelForm):
    name = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Name'
        }
    ))
    domain = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter Domain'
        }
    ))
    VIEWS = (
        ('', 'Please Select'),
        ('1', 'Active'),
        ('0', 'Inactive'),
    )
    state_id = forms.ChoiceField(required = True,choices=VIEWS,widget=forms.Select(
        attrs={
        'class':'form-control'
        }
    ))
    patente = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter patente'
        }
    ))
    class Meta:
        # write the name of models for which the form is made
        model = Agencies    

        fields =["name", "domain", "patente","state_id"]
   
 
        # Custom fields
 
    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(AgencyCreateForm, self).clean()
         
        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        patente = self.cleaned_data.get('patente')

          # conditions to be met for the username length
        if name:

            if len(name) < 3:
                self._errors['name'] = self.error_class([
                    'Minimum 3 characters required'])
        if patente:

            if len(patente)<5:
                self._errors['patente'] = self.error_class([
                    'patente Should Contain a minimum of 5 characters'])

      
 
      
 
        # return any errors if found
        return self.cleaned_data 



