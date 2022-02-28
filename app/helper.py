from django.contrib.auth.decorators import user_passes_test
from app.models import *
import random


def guest_user(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = '/index'

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator
