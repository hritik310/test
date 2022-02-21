from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from app.models import *
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib import auth




# def index(request):
#     context = {}
#     template = loader.get_template('app/index.html')
#     return HttpResponse(template.render(context, request))

def user_login(request):
    if request.method == "POST":
        uname= request.POST.get('username')
        print(uname)
        upass= request.POST.get('password')
        print(upass)
        # a=pod_groups.objects.all()
        # for i in a: 
        #   b=i.id
        if request.method == "POST":
          current_user = request.user.id
    
        user = authenticate(username=uname,password=upass)
        print(user) 
        if user is not None:
          login(request,user)
          return redirect('stripe_checkout')

        else:
          messages.error(request,"Invalid Credential")
          return redirect('/login')
              
    return render(request,"login/login.html")



def userLogout(request):
  auth.logout(request)
  return redirect('/login')
