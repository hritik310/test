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

<<<<<<< HEAD

=======
>>>>>>> 6b039926085fcc963503ca6c99f541d840ec82b2
# from multiselectfield import MultiSelectField
# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
	id = models.AutoField(primary_key=True)
	USER_TYPE_CHOICES = (
        ("superadmin", 0),
        ("admin", 1), 
        ("user", 2), 
    )
	user_type 	= models.IntegerField(choices = USER_TYPE_CHOICES,default="2")
	username 	= models.CharField(_('username'),max_length=255,default="")
	name 		= models.CharField(_('name'),max_length=255,default="")
	owner		= models.CharField(_('owner'),max_length=255,default="")
	tax_id		= models.IntegerField(null=True)
	email 		= models.EmailField(_('email'),unique=True)
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
	passport_upload = models.FileField(null=True, blank=True)
	passport_expiry = models.DateField(_('Date'), default=datetime.date.today)
	name 		= models.CharField(max_length=255,default="")
	country 	= models.CharField(max_length=255,default="")
	phone 		= PhoneField(blank=True, help_text='Contact phone number',default="")
	address		= models.CharField(max_length=255,default="")
	rfc         = models.CharField(max_length=255,default="")
	curp        = models.CharField(max_length=255,default="")
	city        = models.CharField(max_length=255,default="")
	state       = models.CharField(max_length=255,default="")
<<<<<<< HEAD
	passport_expiry	 =models.DateField(null=True)	
	upload_passport_image=models.ImageField(upload_to='profilepic/')

=======
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)

	
>>>>>>> 6b039926085fcc963503ca6c99f541d840ec82b2
	

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


class Pedimentos(models.Model):
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
	year 		= models.IntegerField(max_length=255,default="")
	note	 	= models.CharField(max_length=255,default="")
<<<<<<< HEAD
	paid        = models.IntegerField(blank=True,null=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	
	

=======
	paid        = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)
>>>>>>> 6b039926085fcc963503ca6c99f541d840ec82b2

class Insurance(models.Model):
		INACTIVE = 0
		ACTIVE = 1
		STATUS = (
		    (INACTIVE, _('Inactive')),
		    (ACTIVE, _('Active')),
		)
		Type =    models.CharField(max_length=255,default="")
		policy_number = models.IntegerField(blank=True, null=True)
		date  	= models.DateField()
		ins_name 	= models.CharField(max_length=255,default="")
		days 	= models.IntegerField(max_length=255,default="")
		vin 	= models.CharField(max_length=255,default="")
		make 	= models.CharField(max_length=255,default="")
<<<<<<< HEAD
		paid =   models.IntegerField(blank=True, null=True)
=======
		paid = models.IntegerField(default=0)
>>>>>>> 6b039926085fcc963503ca6c99f541d840ec82b2
		year 	= models.IntegerField(max_length=255,default="")
		created_at = models.DateTimeField(auto_now_add=True,null=True)
		updated_at =  models.DateTimeField(auto_now=True)
		note	= models.CharField(max_length=255,default="")
		created_at = models.DateTimeField(auto_now_add=True)
		updated_at =  models.DateTimeField(auto_now=True)
		

class Temporary_Permits(models.Model):
		INACTIVE = 0
		ACTIVE = 1
		STATUS = (
		    (INACTIVE, _('Inactive')),
		    (ACTIVE, _('Active')),
		)
		permit_date  	= models.DateField()
		permit_name 	= models.CharField(max_length=255,default="")
		permit_hour 	= models.FloatField(max_length=255,default="")
		permit_number 	= models.CharField(max_length=255,default="")
		permit_vin 		= models.CharField(max_length=255,default="")
		permit_make 	= models.CharField(max_length=255,default="")
		permit_year 	= models.IntegerField(max_length=255,default="")
		permit_note		= models.CharField(max_length=255,default="")
		paid            = models.IntegerField(default=0)
		created_at = models.DateTimeField(auto_now_add=True,null=True)
		updated_at =  models.DateTimeField(auto_now=True)


class Released(models.Model):
	date  =  models.DateField()
	file  =  models.CharField(max_length=255,default="")
	name = models.CharField(max_length=255,default="")
	refrence = models.CharField(max_length=255,default="")
	vin  =  models.CharField(max_length=255,default="")
	make = models.CharField(max_length=255,default="")
	year = models.PositiveIntegerField()
	note = models.TextField()
	paid  = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at =  models.DateTimeField(auto_now=True)



class File(models.Model):
	model_id = models.IntegerField()
	model_type = models.CharField(max_length=255,default="")
	file = models.CharField(max_length=255,default="")
	size = models.CharField(max_length=255,default="")
	type_id = models.IntegerField(default=0)

	