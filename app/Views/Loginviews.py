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
          
          return redirect('/signup')
              
    return render(request,"signup/signup.html")



def userLogout(request):
  auth.logout(request)
  return redirect('/signup')


def setting(request):
  return render(request,"login/setting.html")

def update(request):
  a=StripeCustomer.objects.filter(stripeCustomerId=request.user.id)
  show=a.values_list('membershipstatus',flat="true")
  
  if StripeCustomer.objects.filter(stripeCustomerId=request.user.id).exists():
      owner_id=show[0]
  else:
    owner_id=0   
  return render (request,"login/update.html",{'show':owner_id})





