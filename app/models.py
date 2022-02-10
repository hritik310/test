from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.core.validators import validate_comma_separated_integer_list
from phone_field import PhoneField

# Create your models here.
class user(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=200,null=True,unique=True)
    email=models.EmailField(_('email'),unique=True)
    password=models.CharField(max_length=220)
    first_name=models.CharField(max_length=200,null=True)
    last_name=models.CharField(max_length=200,null=True)
    date_of_birth=models.DateField(null=True)
    phone_number=PhoneField(null=True,default=0)
    #address=models.CharField(max_length=100,null=True)
    is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)



    USERNAME_FIELD 	='email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email


