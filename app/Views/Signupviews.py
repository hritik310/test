from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from vote.models import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from vote.forms.user import *
from django.db.models import F


def index(request):   
    context = {'user_list':user.objects.all()}
    return render(request,"pod/p.html",context) 


def create(request):
    if request.method == 'POST':
        accountform = AddCreateForm(request.POST)
        if accountform.is_valid():
            new_user = accountform.save()
            new_user.set_password(
                accountform.cleaned_data.get('password')         
            )
            if accountform.save():
                messages.success(request,'Account Added Successfully.')
                return redirect('/login')
        else:
            return render(request,"signup/create.html",{'form':accountform})

    form = AddCreateForm()
    return render(request,"signup/create.html",{'form':form})