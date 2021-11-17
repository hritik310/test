from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from app.models import *
import random

def guest_user(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = '/home'

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator

def saveMultipleFiles(files,model):
    for file in files:
        fileModel = File()
        fs = FileSystemStorage()
        fileModel.file = fs.save(file.name,file)
        fileModel.model_id = model.id
        fileModel.model_type = model.__class__.__name__
        fileModel.save()



