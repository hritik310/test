
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from pymysql import NULL
from app.models import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from app.forms.user import *
import random
from django.http import JsonResponse
import stripe
from django.conf import settings
from django.views.generic.base import TemplateView
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import pandas as pd
from datetime import datetime
import re
import bs4
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from math import sqrt
from sklearn.metrics import mean_pinball_loss, mean_squared_error
from numpy import asarray
from pysbr import *
import json
import seaborn as sb
import matplotlib.pyplot as mp
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail

stripe.api_key = settings.SECTRET_KEY # new

# print(stripe.api_key)


def index(request):
   
    context = user.objects.all()
    if request.method =="POST":
        messages.success(request,"Contact request submitted successfully")
    return render(request,"signup/home.html",{"context":context}) 

def create(request):
   
    context=user.objects.all()
    if request.method == 'POST':
        accountform = AddCreateForm(request.POST)
        if accountform.is_valid():
            print("True")

            name=request.POST.get("username")
            print(name)
            unique_id = get_random_string(length=5)
            uniqueName=name + unique_id
            accountform.username=uniqueName
            print("accountform",accountform.username)    
            new_user = accountform.save(commit=False)
            new_user.is_active = False
            new_user.save()
           


            new_user.entry_code= uniqueName
                
            
            new_user.set_password(
                accountform.cleaned_data.get('password')         
            )
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('header/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token':account_activation_token.make_token(new_user),
            })
            to_email = accountform.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, 
                        message, 
                        to=[to_email]
            )
           

            a=accountform.save()
            print(a.id)
            email.send()
            messages.success(request,"Thanks for registering with us.Please confirm your email address to complete the registration.",extra_tags='logout')
            return redirect('signup')
              

        else:
            print("False")
            #return HttpResponseRedirect(request.path_info,{'form':accountform})

            return render(request,"signup/signup.html",{'form':accountform,"context":context})

    form = AddCreateForm()
    return render(request,"signup/signup.html",{'form':form,"context":context})


def activate(request, uidb64, token):
    User=get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        users = User.objects.get(id=uid)
        print("hritik")
        print("user",users)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        users = None
        print("hritik")
        print("user",users)
    if users is not None and account_activation_token.check_token(users, token):
        users.is_active = user.objects.filter(id=uid).update(is_active=True)
        login(request, users)
        # messages.success(request,"Successfully Registered")
        return redirect('account')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def account(request):
  
    return render (request,"signup/account.html")


def membership(request):

    return render (request,"signup/buildacc.html")

def updateprofile(request,id):
    custom  = user.objects.get(id=id)
    if request.method == "POST":

        custom.username = request.POST.get('username')
        custom.email = request.POST.get('email')
        custom.phone_number= request.POST.get('phone_number')
        custom.save()
        return redirect('update')


    return render(request,"signup/update.html",{'customer':custom})



def buildmodel(request,id):
    all=Modelvar.objects.all()
    req = request.GET.get('cars')
    print("Request",req)
    st = StripeCustomer.objects.filter(stripeCustomerId = request.user.id).values_list("membershipstatus",flat=True)
    membership=list(st)
    print(membership)
    if 1 in membership:
        if not req:
            req = "nba"
        if req == 'ncaab':
            df = pd.read_csv('totalcsv/mainDSNCAAB.csv')
            # In[19]:


            #sometimes my scripts I run daily have some errors so there are some 
            #nulls that need to be dropped
            #df = df.dropna()


            # In[20]:


            #i always have trouble with the predictions if I dont have this 
            #In there so I add this
            df['num'] = 1


            # In[21]:


            df.columns


            # In[22]:


            #select columns to keep
            #some are needed for building ml. We will offer those
            #some are needed to back test models and test accuracy
            #probably dont need all of these but these will be good to start
            df_away = df[['joinValue', 'homeRank', 'awayRank', 'homeScore',
                'awayScore', 'awayMP', 'awayFG', 'awayFGA', 'awayFGperc', 'away2P',
                'away2PA', 'away2Pperc', 'away3P', 'away3PA', 'away3Pperc', 'awayFT',
                'awayFTA', 'awayFTperc', 'awayORB', 'awayDRB', 'awayTRB', 'awayAST',
                'awaySTL', 'awayBLK', 'awayTOV', 'awayPF', 'awayPTS', 'homeMP',
                'homeFG', 'homeFGA', 'homeFGperc', 'home2P', 'home2PA', 'home2Pperc',
                'home3P', 'home3PA', 'home3Pperc', 'homeFT', 'homeFTA', 'homeFTperc',
                'homeORB', 'homeDRB', 'homeTRB', 'homeAST', 'homeSTL', 'homeBLK',
                'homeTOV', 'homePF', 'homePTS']]


            # In[23]:


          
            amountOfGames = df.shape[0]
            print(amountOfGames)



        else:
           
            all=Modelvar.objects.all()
            a=Modelvar.objects.filter(created_by=request.user.id).values_list("title",flat="True")
            if Modelvar.objects.filter(created_by=request.user.id).exists():
                status=a
                # print("s",status)
            else:
                
                status=0
            var = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)

            car = len(var)

            answers_list = list(var)
            print("answer",answers_list)
            df = pd.read_csv('totalcsv/finalDS.csv')
            co = len(df.columns)
            print("dhfjd",co)

     


            df_away=["Indoor/Outdoor",
                "Temperature",
                "Humidity",
                "Wind",	
                "First Downs",	
                "Rush Attempts",	
                "Rush Yards",	
                "Rush Yards Per Attempt",	
                "Rush TD",	
                "Completions",	
                "Attempts",
                "Pass Yards",	
                "Pass Yards Per Attempt",	
                "Pass Touchdowns",	
                "Interceptions",	
                "Sacked",
                "Sacked Yards",	
                "Net Pass Yards",	
                "Total Yards",	
                "Fumbles",	
                "Fumbles Lost",	
                "Turnovers",
                "Penalties",	
                "Penalty Yards",	
                "Third Downs Converted",	
                "Third Downs Attempted",	
                "Third Down Percentage",	
                "Fourth Downs Converted",	
                "Fourth Downs Attempted",	
                "Fourth Downs Converted",	
                "Time Of Possesion",		
                "QB CAY_PA",	
                "QB Drop Perc",	
                "QB Bad Throw Perc",
                "QB Blitzed",	
                "QB Hurried",	
                "QB Hit",	
                "QB Pressured Perc",	
                "QB Yards Per Scramble"]


        


            #getting shape. We will use this for back testing / training
            amountOfGames = df.shape[0]
            print("dgdg",amountOfGames)




        
    else:
        return redirect('membership') 


    return render(request,"signup/buildmodel.html",{'re':req,"df":list(df_away),"all":all,"amount":amountOfGames})
    # return render(request,"signup/buildmodel.html",{'H':data"df":list(df_away),'status':status,"all":all})
   

def buildmodelStatus(request):
    build = Modelvar()
    build.title=request.GET.get('id')
    print("build",build.title)
    build.created_by = request.user.id
    build.save()
    data = {
    "status":"OK",
    "messages":"You have selected the item",
    "message":"You have Selected the item",
    "value":0,
    }

    return JsonResponse(data)

def buildmodelremove(request):

    b = Modelvar.objects.filter(title =request.GET.get('id'))
    print(b)
    b.delete()
  
    data = {
    "status":"OK",
    }

    return JsonResponse(data)





def buildmodelbutton(request):
    df = pd.read_csv('totalcsv/finalDS.csv')
    value_in=[]
    home_list=[]
    away_list=[]
    df_col=df.columns
    var = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)
    print("variable",var)
    car = len(var)

    answers_list = list(var)
    print("answer",answers_list)
  
    # print(value1)
    for z in answers_list:
        for  i in df_col:  
            if "Home "+z == i or "Away "+z ==i or z ==  i:
                value_in.append(i)
    print(value_in)
    for i in value_in: 
        if i.startswith("Home"):
            home_list.append(i)
        elif i.startswith("Away"):
            away_list.append(i)
            
        else:
    
            home_list.append(i)
            away_list.append(i)
    print(home_list)
    print(away_list)

            
    
    #home model
    #INSERT HOME VARIABLES INTO HERE
    

    home_X = np.asarray(df[home_list])
    print(home_X)

    #STAYS THE SAME
    home_Y = np.asarray(df[['Home Total']])
    
    #away model
    #INSERT AWAY VARIABLES INTO HERE 
    away_X = np.asarray(df[away_list])
    print(away_X)
    
    #STAYS THE SAME
    away_Y = np.asarray(df[[
    'Away Total']])
    
    homeModel = xgb.XGBRegressor()
    awayModel = xgb.XGBRegressor()

    
    print("home",homeModel.fit(home_X,home_Y))
    print("away",awayModel.fit(away_X,away_Y))

    data={"status":"ok"}
    return JsonResponse(data)

        

        
       
def download_file(request):
    filename = "totalcsv/output.csv"
    download_name ="example.csv"
    with open(filename, 'r') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response






def new(request):
    return render(request,"signup/new.html")



def selectvariable(request):
    return render(request,"signup/buildmodel3.html")
def training(request):
    return render(request,"signup/buildmodel4.html")

def modelname(request):
    if request.method == "POST":
        name = Modelname()  
        name.modelname = request.POST.get("modelname")
        name.user_id=request.user.id
        len_model=Modelname.objects.filter(user_id=request.user.id)
        if len(len_model)<=2:
            name.save()
            return redirect('mymodel')
        else:
            print("you can only create 3 model")

    return render(request,"signup/buildmodel5.html")

def mymodel(request):
    val=Modelname.objects.filter(user_id=request.user.id)
    print(val)
    if val:
        print("value")
    else:
        return render(request,"signup/mymodel.html")

    return render(request,"signup/mymodel.html",{"model_name":val})




def send_file(request):
    img = open('resul.png', 'rb')
    dow="h.png" 
    response = HttpResponse(img)
    response['Content-Disposition'] = 'attachment; filename=%s.png' %dow 

    return response

def heatmap(request):
    all=Modelvar.objects.all()
    req = request.GET.get('cars')
    print("Request",req)
    st = StripeCustomer.objects.filter(stripeCustomerId = request.user.id).values_list("membershipstatus",flat=True)
    membership=list(st)
    print(membership)
    if 1 in membership:
        print("1")
        if not req:
            req = "nba"
            
        if req == 'ncaab':    
            print("checkkkk")
            df_away = df[['joinValue', 'homeRank', 'awayRank', 'homeScore',
                'awayScore', 'awayMP', 'awayFG', 'awayFGA', 'awayFGperc', 'away2P',
                'away2PA', 'away2Pperc', 'away3P', 'away3PA', 'away3Pperc', 'awayFT',
                'awayFTA', 'awayFTperc', 'awayORB', 'awayDRB', 'awayTRB', 'awayAST',
                'awaySTL', 'awayBLK', 'awayTOV', 'awayPF', 'awayPTS', 'homeMP',
                'homeFG', 'homeFGA', 'homeFGperc', 'home2P', 'home2PA', 'home2Pperc',
                'home3P', 'home3PA', 'home3Pperc', 'homeFT', 'homeFTA', 'homeFTperc',
                'homeORB', 'homeDRB', 'homeTRB', 'homeAST', 'homeSTL', 'homeBLK',
                'homeTOV', 'homePF', 'homePTS']]

        
            var = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)

            car = len(var)

            answers_list = list(var)
            df = pd.read_csv('mainDSNCAAB.csv')
           
            hriti = df.corr()
            top_ten="" 
            for j in answers_list:
                print("////////////////////////",hriti[j].sort_values(ascending=False)[:10])
                top_ten=hriti[j].sort_values(ascending=False)[:10]
                print("toppppp_tennnnn",top_ten)


            #sometimes my scripts I run daily have some errors so there are some 
            #nulls that need to be dropped
            #df = df.dropna()


            # In[20]:


            #i always have trouble with the predictions if I dont have this 
            #In there so I add this
            df['num'] = 1


            # In[21]:


            df.columns


            amountOfGames = df.shape[0]
            print(amountOfGames)

        else:
            print("why")
            all=Modelvar.objects.all()
            a=Modelvar.objects.filter(created_by=request.user.id).values_list("title",flat="True")
            if Modelvar.objects.filter(created_by=request.user.id).exists():
                status=a
            else:
                
                status=0
            var = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)

            car = len(var)

            answers_lists = list(var)
            print("answer",answers_lists)
            df = pd.read_csv('totalcsv/finalDS.csv')
            # man=df[df.columns[1:]].corr()['home_steals'].sort_values(ascending=False)[:10]
            # print(man)
           
            # hrit = df.corr()
            # top_ten="" 
            # for j in answers_lists:
            #     print(hrit[j].sort_values(ascending=False)[:10])
            #     top_ten=hrit[j].sort_values(ascending=False)[:10]
            #     print("toppppp_tennnnn",top_ten)
            # hrit.to_csv("output.csv")
            # dataplot = sb.heatmap(df.corr(), cmap="YlGnBu", annot=True)
            # dataplot.figure.savefig('result.png')
  
# displaying heatmap
            # mp.show()

         
        
            df_away=df[["Home Team",
            "Away Team",
            "Home Total",
            "Away Total",
            "Total Points",
            "Home _diff",	
            "Indoor/Outdoor",	
            "Temperature",	
            "Humidity",	
            "Wind",	
            "Favorite",	
            "Spread Amount",	
            "Total Line",	
            "Home First Downs",	
            "Home Rush Attempts",	
            "Home Rush Yards",	
            "Home Rush Yards Per Attempt",
            "Home Rush TD",	
            "Home Completions",	
            "Home Attempts",	
            "Home Pass Yards",	
            "Home Pass Yards Per Attempt",
            "Home Pass Touchdowns",	
            "Home Interceptions",	
            "Home Sacked",	
            "Home Sacked Yards",	
            "Home Net Pass Yards",	
            "Home Total Yards",
            "Home Fumbles",	
            "Home Fumbles Lost",	
            "Home Turnovers",	
            "Home Penalties",	
            "Home Penalty Yards",	
            "Home Third Downs Converted",	
            "Home Third Downs Attempted",	
            "Home Third Down Percentage",	
            "Home Fourth Downs Converted",	
            "Home Fourth Downs Attempted",	
            "Home Fourth Downs Converted",	
            "Home Time Of Possesion",	
            "Away First Downs",	
            "Away Rush Attempts",	
            "Away Rush Yards",	
            "Away Rush Yards Per Attempt",	
            "Away Rush TD",	
            "Away Completions",	
            "Away Attempts",	
            "Away Pass Yards",	
            "Away Pass Yards Per Attempt",	
            "Away Pass Touchdowns",	
            "Away Interceptions",	
            "Away Sacked",	
            "Away Sacked Yards",	
            "Away Net Pass Yards",	
            "Away Total Yards",	
            "Away Fumbles",	
            "Away Fumbles Lost",	
            "Away Turnovers",	
            "Away Penalties",	
            "Away Penalty Yards",	
            "Away Third Downs Converted",	
            "Away Third Downs Attempted",	
            "Away Third Down Percentage",
            "Away Fourth Downs Converted",	
            "Away Fourth Downs Attempted",	
            "Away Fourth Down Percentage",	
            "Away Time Of Possesion",	
            "Home Qb Name",	
            "Home QB 1d Perc",	
            "Home QB CAY_PA",	
            "Home QB Drop Perc",	
            "Home QB Bad Throw Perc",	
            "Home QB Blitzed",	
            "Home QB Hurried",	
            "Home QB Hit",	
            "Home QB Pressured Perc",	
            "Home QB Yds Per Scram",	
            "Away Qb Name",	
            "Away QB 1d Perc",	
            "Away QB CAY_PA",	
            "Away QB Drop Perc",	
            "Away QB Bad Throw Perc",	
            "Away QB Blitzed",	
            "Away QB Hurried",	
            "Away QB Hit",	
            "Away QB Pressured Perc",	
            "Away QB Yds Per Scram",
            "Season"]]
    


            #getting shape. We will use this for back testing / training
            amountOfGames = df.shape[0]
            print(amountOfGames)

    else:
        return redirect('membership') 
    return render(request,"signup/buildmodel1.html",{'re':req,"df":list(df_away),"all":all,"amount":amountOfGames})

def minmax(request):
    
    req = request.POST.getlist('minvalue[]')
    print("ss",req)
    df = pd.read_csv('totalcsv/finalDS.csv')

    start = 0
    newdata = []
   
    for i in req:
        start=df.loc[df['Season'] == int(i)] 
        use1 = (len(start))
        newdata.append(use1)
    print(newdata)  
   
    if newdata:
        newlist = sum(newdata)
    else:
        newlist=1100

    data = {
    "status":"OK",
    "dataset":newlist
    }
    return JsonResponse(data)

