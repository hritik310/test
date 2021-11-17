from django.contrib.auth import authenticate, login,logout
from app.models import *
from app.helper import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import redirect


def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))

@guest_user
def userLogin(request):
    if request.method == "POST":
        uname= request.POST.get('username')
        print(uname)
        upass= request.POST.get('password')
        print(upass)
        user = authenticate(username=uname,password=upass)
        if user is not None:
            login(request,user)
            return redirect('/home')

        else:
            messages.error(request,"Invalid Credential")
            return redirect('/login')

    return render(request,"app/login.html")


@login_required
def userLogout(request):
    auth.logout(request)
    return redirect('/login')


@login_required
def home(request):
    return render(request,"home.html",context={"user": request.user})
