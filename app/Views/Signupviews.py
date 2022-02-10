from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from app.models import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from app.forms.user import *
from django.db.models import F
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY # new


def index(request):   
    context = {'user_list':user.objects.all()}
    return render(request,"index.html",context) 


def create(request):
    if request.method == 'POST':
        accountform = AddCreateForm(request.POST)
        if accountform.is_valid():
            new_user = accountform.save()
            users = user.objects.get(id=new_user.id)
            strip_customer = stripe.Customer.create(
                description= users.username,
                email=users.email
            )
            new_user.set_password(
                accountform.cleaned_data.get('password')         
            )

            if accountform.save():
                messages.success(request,'Account Added Successfully.')
                return redirect('login')
        else:
            return render(request,"signup/index.html",{'form':accountform})

    form = AddCreateForm()
    return render(request,"signup/index.html",{'form':form})

# def make(request,id):
#     users = user.objects.get(id=id)
#     strip_customer = stripe.Customer.create(
#         description= users.name,
#         email=users.email
#     )
#     print("see",strip_customer.description)
#     print("email",strip_customer.email)