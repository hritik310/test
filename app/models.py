from pyexpat import model
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
    title=models.CharField(max_length=200,null=True)
    password=models.CharField(max_length=220)
    first_name=models.CharField(max_length=200,null=True)
    last_name=models.CharField(max_length=200,null=True)
    date_of_birth=models.DateField(null=True,blank=True)
    zip=models.IntegerField(max_length=6,null=True)
    address=models.CharField(max_length=200,null=True)
    phone_number=PhoneField(null=True,default=0)
    terms_and_condition=models.BooleanField(default=0,null=False)
    #address=models.CharField(max_length=100,null=True)
    entry_code=models.CharField(max_length=200,null=True)
    is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)


# class store(model.Model):
    

    USERNAME_FIELD 	='username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class StripeCustomer(models.Model):
    #users = models.OneToOneField(to=user, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=300,null=True)
    stripeSubscriptionId = models.CharField(max_length=255,null=True)
    membershipstatus = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username


class Modelvar(models.Model):
    title = models.CharField(max_length=255,default="")
    created_by = models.IntegerField(null=True)
    percent_value = models.IntegerField(null=True)


    # status=models.IntegerField(default=0)

class Modelname(models.Model):
    modelname = models.CharField(max_length=255,null=True,unique=True)
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)


class Var(models.Model):
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Selectvar(models.Model):
    title = models.CharField(max_length=255,default="")
    percent_value = models.IntegerField(null=True)
    varid = models.ForeignKey(Var,on_delete=models.CASCADE,null=True)
