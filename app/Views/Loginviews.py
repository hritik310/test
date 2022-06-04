from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from app.forms.update import userform
from app.models import *
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib import auth
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from app.helper import *
from app.forms.update import *
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import update_session_auth_hash
import pandas as pd




def user_login(request):
    
  
    if request.method == "POST":
        uname= request.POST.get('uname')
        print(uname)
        upass= request.POST.get('psw')
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
          return redirect('sport')
         
        else:
          messages.error(request,"Invalid Credential", extra_tags='login')
          return redirect('/signup')
              
    return render(request,"signup/signup.html")



def userLogout(request):
  auth.logout(request)
  return redirect('/signup')


def setting(request):  
    return render(request,"login/setting.html",)

def update(request,id):
  custom  = user.objects.get(id=id)
  print("custom",custom)
  a=StripeCustomer.objects.filter(stripeCustomerId=request.user.id)
  show=a.values_list('membershipstatus',flat="true")
  
  if StripeCustomer.objects.filter(stripeCustomerId=request.user.id).exists():
      owner_id=show[0]
  else:
    owner_id=0   
  context = {
        "form": userform()
    }
  
  accountform =  userform(instance=custom)
  print("request",request.user)
  if request.method == "POST":
    accountform = userform(request.POST,instance=custom)
    if accountform.is_valid():
        print("True")
        accountform.save()

    
    else:      
      print("false")
      return render(request,"login/update.html",{'form':accountform,"context":context})
  
  
  return render (request,"login/update.html",{'show':owner_id,'customer':custom,'form':accountform})

def passwordchange(request,id):
  custom = user.objects.get(id=id)

  if request.method == 'POST':
    # old_password = request.POST.get("old_password")
    new_password=request.POST.get("new_password")
    confirm=request.POST.get("confirm")
    noob = request.user
    if new_password and confirm:
      if new_password != confirm:
        messages.error(request, "Your new password not match the confirm password !")
      else:  
        u=user.objects.get(username=noob)   
        u.set_password(new_password)
        u.save()
        update_session_auth_hash(request,u)
        messages.success(request, 'Your password has been changed successfuly.!')   
        return redirect("passwordchange",id=id) 

    else:
      messages.error(request, 'All fields are required.')
    
  
    
            
  return render(request,"login/changepassword.html")








