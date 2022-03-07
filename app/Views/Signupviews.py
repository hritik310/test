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
from django.db.models import F
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
from sklearn.metrics import mean_squared_error
from numpy import asarray

stripe.api_key = settings.SECTRET_KEY # new
print(stripe.api_key)


def index(request):   
    df = ["datetime",
    "spread / total",
    "over_under_total",
    "decimal odds",
    "american odds",
    "event",
    "participant score",
    "participant",
    "participant full name",
    "underdog score",
    "underdog team",
    "underdog abb",
    "home",
    "away",
    "dateForJoin",
    "away_assist_percentage",
    "away_assists",
    "away_block_percentage",
    "away_blocks",
    "away_defensive_rating",
    "away_defensive_rebound_percentage",
    "away_defensive_rebounds",
    "away_effective_field_goal_percentage",
    "away_field_goal_attempts",
    "away_field_goal_percentage",
    "away_field_goals",
    "away_free_throw_attempt_rate",
    "away_free_throw_attempts",
    "away_free_throw_percentage",
    "away_free_throws",
    "away_losses",
    "away_minutes_played",
    "away_offensive_rating",
    "away_offensive_rebound_percentage",
    "away_offensive_rebounds",
    "away_personal_fouls",
    "away_points",
    "away_steal_percentage",
    "away_steals",
    "away_three_point_attempt_rate",
    "away_three_point_field_goal_attempts",
    "away_three_point_field_goal_percentage",
    "away_three_point_field_goals",
    "away_total_rebound_percentage",
    "away_total_rebounds",
    "away_true_shooting_percentage",
    "away_turnover_percentage",
    "away_turnovers",
    "away_two_point_field_goal_attempts",
    "away_two_point_field_goal_percentage",
    "away_two_point_field_goals",
    "away_wins",
    "home_assist_percentage",
    "home_assists",
    "home_block_percentage",
    "home_blocks",
    "home_defensive_rating",
    "home_defensive_rebound_percentage",
    "home_defensive_rebounds",
    "home_effective_field_goal_percentage",
    "home_field_goal_attempts",
    "home_field_goal_percentage",
    "home_field_goals",
    "home_free_throw_attempt_rate",
    "home_free_throw_attempts",
    "home_free_throw_percentage",
    "home_free_throws",
    "home_losses",
    "home_minutes_played",
    "home_offensive_rating",
    "home_offensive_rebound_percentage",
    "home_offensive_rebounds",
    "home_personal_fouls",
    "home_points",
    "home_steal_percentage",
    "home_steals",
    "home_three_point_attempt_rate",
    "home_three_point_field_goal_attempts",
    "home_three_point_field_goal_percentage",
    "home_three_point_field_goals",
    "home_total_rebound_percentage",
    "home_total_rebounds",
    "home_true_shooting_percentage",
    "home_turnover_percentage",
    "home_turnovers",
    "home_two_point_field_goal_attempts",
    "home_two_point_field_goal_percentage",
    "home_two_point_field_goals",
    "home_wins",
    "location",
    "losing_abbr",
    "losing_name",
    "pace",
    "winner",
    "winning_abbr",
    "winning_name",
    "num"]
    for i in df:
        print(i)
        a=random.choice(i) 
        print(a)
    context = {'user_list':user.objects.all()}
    if request.method =="POST":
        messages.success(request,"Contact request submitted successfully")
    return render(request,"signup/home.html",context) 

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
        return redirect('/')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def updateprofile(request,id):
    custom  = user.objects.get(id=id)
    if request.method == "POST":

        custom.username = request.POST.get('username')
        custom.email = request.POST.get('email')
        custom.phone_number= request.POST.get('phone_number')
        custom.save()
        return redirect('update')


    return render(request,"signup/update.html",{'customer':custom})



def buildmodel(request):
    df = pd.read_csv('finalDS.csv')

    df = df.dropna()

    df = df.replace(to_replace ="New Orleans",value ="New Orleans Pelicans")
    df = df.replace(to_replace ="L.A. Clippers Clippers",value ="Los Angeles Clippers")
    df = df.replace(to_replace ="L.A. Clippers",value ="Los Angeles Clippers")
    df = df.replace(to_replace ="LA Clippers",value ="Los Angeles Clippers")
    df = df.replace(to_replace ="Oklahoma City",value ="Oklahoma City Thunder")
    df = df.replace(to_replace ="Golden State",value ="Golden State Warriors")
    df = df.replace(to_replace ="New York",value ="New York Knicks")
    df = df.replace(to_replace ="L.A. Lakers Lakers",value ="Los Angeles Lakers")
    df = df.replace(to_replace ="LA Lakers",value ="Los Angeles Lakers")
    df = df.replace(to_replace ="L.A. Lakers",value ="Los Angeles Lakers")
    df = df.replace(to_replace ="San Antonio",value ="San Antonio Spurs")


    df['num'] = 1


    df = df[["datetime",
    "spread / total",
    "over_under_total",
    "decimal odds",
    "american odds",
    "event",
    "participant score",
    "participant",
    "participant full name",
    "underdog score",
    "underdog team",
    "underdog abb",
    "home",
    "away",
    "dateForJoin",
    "away_assist_percentage",
    "away_assists",
    "away_block_percentage",
    "away_blocks",
    "away_defensive_rating",
    "away_defensive_rebound_percentage",
    "away_defensive_rebounds",
    "away_effective_field_goal_percentage",
    "away_field_goal_attempts",
    "away_field_goal_percentage",
    "away_field_goals",
    "away_free_throw_attempt_rate",
    "away_free_throw_attempts",
    "away_free_throw_percentage",
    "away_free_throws",
    "away_losses",
    "away_minutes_played",
    "away_offensive_rating",
    "away_offensive_rebound_percentage",
    "away_offensive_rebounds",
    "away_personal_fouls",
    "away_points",
    "away_steal_percentage",
    "away_steals",
    "away_three_point_attempt_rate",
    "away_three_point_field_goal_attempts",
    "away_three_point_field_goal_percentage",
    "away_three_point_field_goals",
    "away_total_rebound_percentage",
    "away_total_rebounds",
    "away_true_shooting_percentage",
    "away_turnover_percentage",
    "away_turnovers",
    "away_two_point_field_goal_attempts",
    "away_two_point_field_goal_percentage",
    "away_two_point_field_goals",
    "away_wins",
    "home_assist_percentage",
    "home_assists",
    "home_block_percentage",
    "home_blocks",
    "home_defensive_rating",
    "home_defensive_rebound_percentage",
    "home_defensive_rebounds",
    "home_effective_field_goal_percentage",
    "home_field_goal_attempts",
    "home_field_goal_percentage",
    "home_field_goals",
    "home_free_throw_attempt_rate",
    "home_free_throw_attempts",
    "home_free_throw_percentage",
    "home_free_throws",
    "home_losses",
    "home_minutes_played",
    "home_offensive_rating",
    "home_offensive_rebound_percentage",
    "home_offensive_rebounds",
    "home_personal_fouls",
    "home_points",
    "home_steal_percentage",
    "home_steals",
    "home_three_point_attempt_rate",
    "home_three_point_field_goal_attempts",
    "home_three_point_field_goal_percentage",
    "home_three_point_field_goals",
    "home_total_rebound_percentage",
    "home_total_rebounds",
    "home_true_shooting_percentage",
    "home_turnover_percentage",
    "home_turnovers",
    "home_two_point_field_goal_attempts",
    "home_two_point_field_goal_percentage",
    "home_two_point_field_goals",
    "home_wins",
    "location",
    "losing_abbr",
    "losing_name",
    "pace",
    "winner",
    "winning_abbr",   
    "winning_name",
    "num"]]
    # for i in list(df):
    #     print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii",i)
    #     sh=i
    # a=random.sample(list(df),12) 
    # print("ssssssssssssssssssssssssssssssss",a)



    #getting shape. We will use this for back testing / training
    amountOfGames = df.shape[0]




    df['actual_total_points'] = df['home_points'] + df['away_points']


    # In[117]:


    backTest = [10,25,50,100]
    var = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)
    answers_list = list(var)
    print(answers_list)
 

    # show=var.values_list("title",flat=True)
    # print("show",show)
    # for i in show:
    #     lst=list(i)
        #print(lst)
    for i in backTest:
        training = df[:amountOfGames-i]
        print(training.shape)
        predictionGames = df[i*-1:]
        print(predictionGames.shape)
        wins = 0
        losses = 0
        ties = 0
        
        total_wins = 0
        total_losses = 0
        total_ties = 0
        
        #as a user selects and drops a variable it will be added and dropped 
        # to this list. This list is the list of variables used in the model
        if len(answers_list)==12:
            modelVars=answers_list
         
        else:
            modelVars=['num',
            'away_defensive_rating',    
            'away_offensive_rating',
            'away_three_point_attempt_rate',
            'away_true_shooting_percentage',
            'away_turnover_percentage',
            'home_defensive_rating',
            'home_offensive_rating',
            'home_three_point_attempt_rate',
            'home_true_shooting_percentage',
            'home_turnover_percentage',
            'pace']
    
        #we build two models but kind of use them just as one. We have the same
        #variables in both just a different target variable
        X = np.asarray(training[modelVars])
        Y_home=np.asarray(training['home_points'])
        Y_away=np.asarray(training['away_points'])
        #fit the model for home_points and away_points

        home_model = xgb.XGBRegressor()
        away_model = xgb.XGBRegressor()


        home_model.fit(X,Y_home)
        away_model.fit(X,Y_away)
        
        
        
        
        
        for index, row in predictionGames.iterrows():
            home = row['home']
            away = row['away']

            
           
            homeTeam = df.loc[df['home']==home]
            awayTeam = df.loc[df['away']==away]
            #get the averages of the playing
            #we use averages to make predictions
            homeTeamAverages = homeTeam.mean()
            awayTeamAverages = awayTeam.mean()
            
            #NEED HELP HERE
            #so the user adds the variables into the list modelVars
            #but I am not sure how we can dynamically use that list to 
            #select them from the averages dataframe we create.
            row2 = [1,
              awayTeamAverages['away_defensive_rating'],
              awayTeamAverages['away_offensive_rating'],
              awayTeamAverages['away_three_point_attempt_rate'],
              awayTeamAverages['away_true_shooting_percentage'],
              awayTeamAverages['away_turnover_percentage'],
              homeTeamAverages['home_defensive_rating'],
               homeTeamAverages['home_offensive_rating'],
               homeTeamAverages['home_three_point_attempt_rate'],
               homeTeamAverages['home_true_shooting_percentage'],
               homeTeamAverages['home_turnover_percentage'],
               (homeTeamAverages['pace'] + awayTeamAverages['pace'])/2,
                   ]
        
            new_data = asarray([row2])
            home_points = home_model.predict(new_data)[0]
          
            away_points = away_model.predict(new_data)[0]

            prediction_total_points = home_points + away_points
            
        
            if prediction_total_points>row['over_under_total']:
                if row['actual_total_points']>row['over_under_total']:
                    total_wins = total_wins + 1
                elif row['actual_total_points']==row['over_under_total']:
                    total_ties = total_ties + 1
                else:
                    total_losses = total_losses + 1
            
            if prediction_total_points<row['over_under_total']:
                if row['actual_total_points']<row['over_under_total']:
                    total_wins = total_wins + 1
                elif row['actual_total_points']==row['over_under_total']:
                    total_ties = total_ties + 1
                else:
                    total_losses = total_losses + 1
            
            
                
            
            
            
            #code to get the record for the model
            if home == row['participant full name']:
               
        
        
                point_diff = home_points-away_points
             

        
                if point_diff > abs(row['spread / total']):
                    if row['participant score']-row['underdog score']>abs(row['spread / total']):
                         wins = wins + 1
                    elif row['participant score']-row['underdog score']==abs(row['spread / total']):
                        ties = ties + 1

                    else:
                        losses = losses + 1


                   
            
                if point_diff < abs(row['spread / total']):
                    if row['participant score']-row['underdog score']<abs(row['spread / total']):
                        wins = wins + 1
                
                    elif row['participant score']-row['underdog score']==abs(row['spread / total']):
                        ties = ties + 1
                        
                    else:                
                        losses = losses + 1


                
        
                
            if away == row['participant full name']:
                
                
                point_diff = home_points-away_points
                
                if point_diff > abs(row['spread / total']):
                    if row['participant score']-row['underdog score']>row['spread / total']:
                        wins = wins + 1
                           
                        
                        
                        
                    elif row['participant score']-row['underdog score']==row['spread / total']:
                        ties = ties + 1
                    
                    
                    else:
                        losses = losses + 1


                        
                        
                if point_diff < abs(row['spread / total']):
                    if row['participant score']-row['underdog score']<abs(row['spread / total']):
                        wins = wins + 1
                        
                   
                    elif row['participant score']-row['underdog score']==abs(row['spread / total']):
                        ties = ties + 1

                    else:
                        losses = losses + 1
        
        
        print('Last ' + str(abs(i)) + ' games')
        print('wins over/under: ' + str(total_wins))
        print('losses over/under: ' + str(total_losses))
        print('ties over/under: ' + str(total_ties))
        games = abs(i)-total_ties
        print('win% over/under: ' + str(total_wins/games))
        print('             ')               
                        
        print('Last ' + str(abs(i)) + ' games')
        print('wins spread: ' + str(wins))
        print('losses spread: ' + str(losses))
        print('ties spread: ' + str(ties))
        games = abs(i)-ties
        print('win% spread: ' + str(wins/games))
        print('             ')


    return render(request,"signup/buildmodel.html",{"df":list(df)})


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

    b = Modelvar.objects.filter(title =request.GET.get('id')).last()
    b.delete()
    print(b)
  
    data = {
    "status":"OK"
    }

    return JsonResponse(data)


