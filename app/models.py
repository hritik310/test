from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import CustomUserManager
from django_countries.fields import CountryField
from phone_field import PhoneField

# from multiselectfield import MultiSelectField
# Create your models here.


class Company(models.Model):
	company_name=models.CharField(max_length=255,default="")
	company_description=models.CharField(max_length=255,default="")


class User(AbstractBaseUser,PermissionsMixin):
	id = models.AutoField(primary_key=True)
	USER_TYPE_CHOICES = (
        ("superadmin", 0),
        ("provider", 1), 
        ("user", 2), 
    )
	company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True)
	user_type 	= models.IntegerField(choices = USER_TYPE_CHOICES,default="2")
	username 	= models.CharField(_('username'),max_length=255,default="")
	email 		= models.EmailField(_('email'),unique=True)
	phone 		= PhoneField(blank=True, help_text='Contact phone number',default="")
	is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
	is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)


	#date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	USERNAME_FIELD 	='email'
	objects 		= CustomUserManager()

	def __str__(self):
		return self.email
# Create your models here.



class Customer(models.Model):
	passport_id	= models.PositiveIntegerField(default=1)
	passport_upload = models.FileField(null=True)
	passport_expiry = models.DateField(_('Date'), default=datetime.date.today)
	name 		= models.CharField(max_length=255,default="")
	country 	= models.CharField(max_length=255,default="")
	phone 		= PhoneField(blank=True, help_text='Contact phone number',default="")
	email       = models.EmailField(max_length=255,default="")
	address		= models.CharField(max_length=255,default="")
	rfc         = models.CharField(max_length=255,default="")
	curp        = models.CharField(max_length=255,default="")
	city        = models.CharField(max_length=255,default="")
	state       = models.CharField(max_length=255,default="")
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

	
	

class Agencies(models.Model):
	INACTIVE = 0
	ACTIVE = 1
	STATUS = (
        (INACTIVE, _('Inactive')),
        (ACTIVE, _('Active')),
    )
	name 	= models.CharField(max_length=255,default="")
	domain 	= models.CharField(max_length=255,default="")
	active  = models.IntegerField(default=0, choices=STATUS)
	patente = models.CharField(max_length=255,default="")
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)


class Pedimentos(models.Model):
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	refrence_id 	= models.IntegerField(max_length=11,default="")
	pedimento_no 	= models.IntegerField()
	date  			= models.DateField()
	importer 		= models.CharField(max_length=255,default="")
	office 			= models.CharField(max_length=255,default="")
	signature 		= models.CharField(max_length=255,default="")
	payment 		= models.FloatField(max_length=255,default="")
	cove 			= models.CharField(max_length=255,default="")
	doda	 		= models.CharField(max_length=255,default="")
	ready 			= models.BooleanField()
	remarks         = models.CharField(max_length=255,default="")
	lock1           = models.CharField(max_length=255,default="")
	lock2           = models.CharField(max_length=255,default="")
	lock3           = models.CharField(max_length=255,default="")
	lock4           = models.CharField(max_length=255,default="")
	lock5           = models.CharField(max_length=255,default="")
	lock6           = models.CharField(max_length=255,default="")
	lock7           = models.CharField(max_length=255,default="")
	lock8           = models.CharField(max_length=255,default="")
	supplier        = models.CharField(max_length=255,default="")

	document        = models.ImageField(upload_to='profilepic/', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)

class Inventories(models.Model):

    pedimentorid = models.ForeignKey(Pedimentos, on_delete=models.CASCADE,null=True)
    order_no = models.IntegerField(max_length=11,default="")
    quantity = models.IntegerField(max_length=11,default="")
    unit_type = models.IntegerField(max_length=11,default="")
    vechicle = models.CharField(max_length=255,default="")
    description = models.CharField(max_length=255,default="")
    price = models.FloatField(max_length=255,default="")
    price_total= models.FloatField(max_length=255,default="")


class Shipper_Exports(models.Model):
	INACTIVE = 0
	ACTIVE = 1
	STATUS = (
        (INACTIVE, _('Inactive')),
        (ACTIVE, _('Active')),
    )
	itn 		= models.CharField(max_length=255,default="")
	date  		= models.DateField()
	refrence 	= models.CharField(max_length=255,default="")
	name 		= models.CharField(max_length=255,default="")
	vin 		= models.CharField(max_length=255,default="")
	make 		= models.CharField(max_length=255,default="")
	year 		= models.IntegerField(max_length=4,default="")
	note	 	= models.CharField(max_length=255,default="")
	paid        = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Insurance(models.Model):
		INACTIVE = 0
		ACTIVE = 1
		STATUS = (
		    (INACTIVE, _('Inactive')),
		    (ACTIVE, _('Active')),
		)
		created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
		Type =    models.CharField(max_length=255,default="")
		insurer = models.CharField(max_length=255,default="")
		policy_number = models.CharField(max_length=255,default="")
		date  	= models.DateField()
		ins_name 	= models.CharField(max_length=255,default="")
		days 	= models.IntegerField(max_length=255,default="")
		vin 	= models.CharField(max_length=255,default="")
		make 	= models.CharField(max_length=255,default="")
		paid = models.IntegerField(default=0)
		year 	= models.IntegerField(max_length=255,default="")
		created_at = models.DateTimeField(auto_now_add=True,null=True)
		updated_at =  models.DateTimeField(auto_now=True)
		note	= models.CharField(max_length=255,default="")

class Temporary_Permits(models.Model):
		INACTIVE = 0
		ACTIVE = 1
		STATUS = (
		    (INACTIVE, _('Inactive')),
		    (ACTIVE, _('Active')),
		)
		created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
		permit_date  	= models.DateField()
		permit_name 	= models.CharField(max_length=255,default="")
		permit_hour 	= models.IntegerField(max_length=255,default="")
		permit_number 	= models.CharField(max_length=255,default="")
		permit_vin 		= models.CharField(max_length=255,default="")
		permit_make 	= models.CharField(max_length=255,default="")
		permit_year 	= models.IntegerField(max_length=4,default="")
		permit_note		= models.CharField(max_length=255,default="")
		paid            = models.IntegerField(default=0)
		created_at = models.DateTimeField(auto_now_add=True,null=True)
		updated_at =  models.DateTimeField(auto_now=True)


class Released(models.Model):
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	date  =  models.DateField()
	file  =  models.CharField(max_length=255,default="")
	name = models.CharField(max_length=255,default="")
	itn = models.CharField(max_length=255,default="")
	vin  =  models.CharField(max_length=255,default="")
	make = models.CharField(max_length=255,default="")
	year = models.PositiveIntegerField()
	scan = models.FileField(null=True)
	note = models.TextField()
	paid  = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)

class Provider(models.Model):
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	name = models.CharField(max_length=255,default="")
	owner = models.CharField(max_length=255,default="")
	email = models.EmailField(unique=True)
	tax_id = models.IntegerField()






class userPermission(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True)

	shipper_Exports=models.IntegerField(default=1)
	pedimentos=models.IntegerField(default=1)
	temporary_Permits= models.IntegerField(default=1)
	customer=models.IntegerField(default=1)
	insurance=models.IntegerField(default=1)
	released=models.IntegerField(default=1)
	catalogs=models.IntegerField(default=1)
	reports=models.IntegerField(default=1)
	validate=models.IntegerField(default=1)




class File(models.Model):
	model_id = models.IntegerField()
	model_type = models.CharField(max_length=255,default="")
	file = models.CharField(max_length=255,default="")
	size = models.CharField(max_length=255,default="")
	type_id = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at =  models.DateTimeField(auto_now=True)

	