
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
from pysbr import *
import json
import seaborn as sb
import matplotlib.pyplot as mp
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from sportsipy.nfl.boxscore import Boxscores

stripe.api_key = settings.SECTRET_KEY # new

#   (stripe.api_key)


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

            name=request.POST.get("username")
            unique_id = get_random_string(length=5)
            uniqueName=name + unique_id
            accountform.username=uniqueName   
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
      
            email.send()
            messages.success(request,"Thanks for registering with us.Please confirm your email address to complete the registration.",extra_tags='logout')
            return redirect('signup')
              

        else:
           
            #return HttpResponseRedirect(request.path_info,{'form':accountform})

            return render(request,"signup/signup.html",{'form':accountform,"context":context})

    form = AddCreateForm()
    return render(request,"signup/signup.html",{'form':form,"context":context})


def activate(request, uidb64, token):
    User=get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        users = User.objects.get(id=uid)
       
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        users = None
       
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




def buildmodel(request,id):
    all=Modelvar.objects.all()
    req = request.GET.get('cars') 
    # print(newdata.query)
   
    st = StripeCustomer.objects.filter(stripeCustomerId = request.user.id).values_list("membershipstatus",flat=True)
    membership=list(st)
    
    if 1 in membership:
            
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
        df = pd.read_csv('totalcsv/finalDS1.csv')
        co = len(df.columns)

    


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
            "QB Yds Per Scram"]


        


        #getting shape. We will use this for back testing / training
        amountOfGames = df.shape[0]
     




        
    else:
        return redirect('membership') 


    return render(request,"signup/buildmodel.html",{'re':req,"df":list(df_away),"all":all,"amount":amountOfGames})
    # return render(request,"signup/buildmodel.html",{'H':data"df":list(df_away),'status':status,"all":all})
   
import random
def buildmodelStatus(request):
    build1=Modelvar()
    n = random.randint(0,10000)
    random_val="f" + str(n)
    build = Modelvar.objects.all().last()   
    if build:
        if build.modelname_id.isnumeric(): 
            build1.title=request.GET.get('id')
            build1.modelname_id=random_val
            build1.created_by = request.user.id
            build1.save()  
        else:   
            build1.title=request.GET.get('id')
            build1.created_by = request.user.id
            build1.modelname_id=random_val
            build1.save() 
    else:
        build1.title=request.GET.get('id')
        build1.created_by = request.user.id
        build1.modelname_id=random_val
        build1.save() 

    data = {
    "status":"OK",
    "messages":"You have selected the item",
    "message":"You have Selected the item",
    "value":0,
    }

    return JsonResponse(data)

def buildmodelremove(request):

    b = Modelvar.objects.filter(title =request.GET.get('id'))

    b.delete()
  
    data = {
    "status":"OK",
    }

    return JsonResponse(data)

def buildmodelUpdate(request):
    build1=Modelvar()

       
    build1.title=request.GET.get('id')
    build1.created_by = request.user.id
    build1.modelname_id=request.GET.get('modelname_id')
    build1.status = 1
    build1.save() 

    data = {
    "status":"OK",
    "messages":"You have selected the item",
    "message":"You have Selected the item",
    "value":0,
    }

    return JsonResponse(data)

def buildmodelremove(request):

    b = Modelvar.objects.filter(title =request.GET.get('id'))

    b.delete()
  
    data = {
    "status":"OK",
    }

    return JsonResponse(data)





def buildmodelbutton(request):
    df = pd.read_csv('totalcsv/finalDS1.csv')
    value_in=[]
    home_list=[]
    away_list=[]
    df_col=df.columns
    var = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)
   
    car = len(var)

    answers_list = list(var)

  
    # print(value1)
    for z in answers_list:
        for  i in df_col:  
            if "Home "+z == i or "Away "+z ==i or z ==  i:
                value_in.append(i)
   
    for i in value_in: 
        if i.startswith("Home"):
            home_list.append(i)
        elif i.startswith("Away"):
            away_list.append(i)
            
        else:
    
            home_list.append(i)
            away_list.append(i)

            
    
    #home model
    #INSERT HOME VARIABLES INTO HERE
    

    home_X = np.asarray(df[home_list])
    
  
   

    #STAYS THE SAME
    home_Y = np.asarray(df[['Home Total']])
   
  
    
    #away model
    #INSERT AWAY VARIABLES INTO HERE 
    away_X = np.asarray(df[away_list])
    
    #STAYS THE SAME
    away_Y = np.asarray(df[[
    'Away Total']])
    
    homeModel = xgb.XGBRegressor()
    awayModel = xgb.XGBRegressor()

    
    homeModel.fit(home_X,home_Y)
    awayModel.fit(away_X,away_Y)

    backTest = [10,25,50,100]
    gameinfo =[]
    for i in backTest:
        seenAverages = df[:-i]
        predictionGames = df[-i:]

        
        spreadWins = 0
        spreadLosses = 0
        spreadTies = 0
        
        overUnderWins = 0
        overUnderLosses = 0
        overUnderTies = 0
        
        moneylineWins = 0
        moneylineLosses = 0
        moneylineTies = 0
        
        
        for index,row in predictionGames.iterrows():
            homeTeamPlaying = row['Home Team']
            awayTeamPlaying = row['Away Team']
            
            homeTeamActualPoints = row['Home Total']
            awayTeamActualPoints = row['Away Total']

            totalActualPoints = row['Total Points']
            
            favoriteTeam = row['Favorite']
            spreadLine = row['Spread Amount']
            totalLine = row['Total Line']
            
            homeTeamStats = df.loc[df['Home Team'] == homeTeamPlaying]
            homeTeamStatsAvg = homeTeamStats.mean()
            
            awayTeamStats = df.loc[df['Away Team'] == awayTeamPlaying]
            awayTeamStatsAvg = awayTeamStats.mean()
            
            
            #USE HOME DATA VARS
            homeData =[]
            for q in home_list:
                homeData.append(homeTeamStatsAvg[q])
                # homeTeamStatsAvg['Home Pass Touchdowns'],
                # homeTeamStatsAvg['Home Total']

            
            
            #USE AWAY DATA VARS
            awayData =[]
            for j in away_list:
                awayData.append(awayTeamStatsAvg[j])
        
            
            homeVarsList = np.asarray([homeData])
            awayVarsList = np.asarray([awayData])
            
            homePrediction = homeModel.predict(homeVarsList)
            awayPrediction = awayModel.predict(awayVarsList)
            predictionDifference = homePrediction[0]-awayPrediction[0]
            predictionTotal = homePrediction[0]+awayPrediction[0]
            

            
            if homeTeamPlaying == favoriteTeam and predictionDifference >= spreadLine:
                #print('home team favorite and predicted home to cover')
                if (homeTeamActualPoints - awayTeamActualPoints) > spreadLine:
                    spreadWins = spreadWins + 1
                elif (homeTeamActualPoints - awayTeamActualPoints) == spreadLine:
                    spreadTies = spreadTies + 1
                else:
                    spreadLosses = spreadLosses + 1
                
                
            elif homeTeamPlaying == favoriteTeam and predictionDifference <= spreadLine:
                #print('home team favorite and predicted away to cover')
                if (homeTeamActualPoints - awayTeamActualPoints) < spreadLine:
                    spreadWins = spreadWins + 1
                elif (homeTeamActualPoints - awayTeamActualPoints) == spreadLine:
                    spreadTies = spreadTies + 1
                else:
                    spreadLosses = spreadLosses + 1
                
                
            elif awayTeamPlaying == favoriteTeam and abs(predictionDifference) >= spreadLine:
                #print('away team favorite and predicted away to cover')
                if (awayTeamActualPoints - homeTeamActualPoints) > spreadLine:
                    spreadWins = spreadWins + 1
                elif (awayTeamActualPoints - homeTeamActualPoints) == spreadLine:
                    spreadTies = spreadTies + 1
                else:
                    spreadLosses = spreadLosses + 1
                
                
            elif awayTeamPlaying == favoriteTeam and abs(predictionDifference) <= spreadLine:
                #print('away team favorite and predicted home to cover')
                if (awayTeamActualPoints - homeTeamActualPoints) < spreadLine:
                    spreadWins = spreadWins + 1
                elif (awayTeamActualPoints - homeTeamActualPoints) == spreadLine:
                    spreadTies = spreadTies + 1
                else:
                    spreadLosses = spreadLosses + 1
                    

            if predictionTotal>totalLine:
                if totalActualPoints>totalLine:
                    overUnderWins = overUnderWins+1
                elif totalActualPoints == totalLine:
                    overUnderTies = overUnderTies+1
                else:
                    overUnderLosses = overUnderLosses + 1
            elif predictionTotal<totalLine:
                if totalActualPoints<totalLine:
                    overUnderWins = overUnderWins+1
                elif totalActualPoints == totalLine:
                    overUnderTies = overUnderTies+1
                else:
                    overUnderLosses = overUnderLosses + 1
            
            
            
            
            if homePrediction > awayPrediction:
                if homeTeamActualPoints-awayTeamActualPoints>0:
                    moneylineWins = moneylineWins + 1
                elif homeTeamActualPoints-awayTeamActualPoints==0:
                    moneylineTies = moneylineTies + 1
                    # print(homePrediction[0])
                    # print(awayPrediction[0])
                    # print(actualPointsDiff)
                else:
                    moneylineLosses = moneylineLosses + 1
            
            elif homePrediction < awayPrediction:
                if homeTeamActualPoints-awayTeamActualPoints<0:
                    moneylineWins = moneylineWins + 1
                elif homeTeamActualPoints-awayTeamActualPoints==0:
                    moneylineTies = moneylineTies + 1
                else:
                    moneylineLosses = moneylineLosses + 1
            
             
            
        spreadgames = 'Last ' + str(abs(i)) + ' games' 
        spreadwins = str(spreadWins)
        spreadloss = str(spreadLosses)
        spreadties=str(spreadTies)
        
        
        overunderwins=str(overUnderWins)
        overunderloss = str(overUnderLosses)
        overunderties = str(overUnderTies)

        
        moneylinewins =str(moneylineWins)
        moneylineloss = str(moneylineLosses)
        moneylineties =str(moneylineTies)
        data={
            "spreadgames":spreadgames,
            'spreadwins':spreadwins,
            'spreadloss':spreadloss,
            'spreadties':spreadties,
            'overunderwins':overunderwins,
            'overunderloss':overunderloss,
            'overunderties':overunderties,
            'moneylinewins':moneylinewins,
            'moneylineloss':moneylineloss,
           'moneylineties':moneylineties
        }

        gameinfo.append(data)

    upcomingGames = Boxscores(1, 2022)
    # Prints a dictionary of all matchups for week 1 of 2017
    upcomingGames = upcomingGames.games

    dates = upcomingGames.keys()
    keys = []
    for key in dates:
        keys.append(key)


    homeName = []
    awayName = []

    for b in keys:
        i = 0
        while i < len(upcomingGames[b]):
            homeName.append(upcomingGames[b][i]['home_name'])
            awayName.append(upcomingGames[b][i]['away_name'])        
            
            
            i = i + 1
            
    data = {
        'Home Team':homeName,
        'Away Team':awayName
    }

    thisWeeksGames = pd.DataFrame(data)

    predict_list=[]
    for index, row in thisWeeksGames.iterrows():
        homeTeamPlaying = row['Home Team']
        awayTeamPlaying = row['Away Team']
        
        homeTeamStats = df.loc[df['Home Team'] == homeTeamPlaying]
        homeTeamStatsAvg = homeTeamStats.mean()
            
        awayTeamStats = df.loc[df['Away Team'] == awayTeamPlaying]
        awayTeamStatsAvg = awayTeamStats.mean()
        
        #HOME VARS THAT USER SELECTS GOES HERE
        
        homeData =[]
        for i in home_list:
            homeData.append(homeTeamStatsAvg[i])
            #USE AWAY DATA VARS
        awayData=[]
        for j in away_list:
            awayData.append(awayTeamStatsAvg[j])
            
        homeVarsList = np.asarray([homeData])
        awayVarsList = np.asarray([awayData])
            
        homePrediction = homeModel.predict(homeVarsList)
        awayPrediction = awayModel.predict(awayVarsList)
        
        show=row['Home Team'] + ' ' + str(round(homePrediction[0])) + ' ' + row['Away Team'] + ' ' +  str(round(awayPrediction[0]))
        predict_list.append(show)
        
   
    games2022 = Boxscores(1,2022,18)

    games2022 = games2022.games

    dates2022 = games2022.keys()
    keys2022 = []
    for key in dates2022:
        keys2022.append(key)


    homeName2022 = []
    awayName2022 = []

    for b in keys2022:
        i = 0
        while i < len(games2022[b]):
            homeName2022.append(games2022[b][i]['home_name'])
            awayName2022.append(games2022[b][i]['away_name'])        
            
            
            i = i + 1
            
    data2022 = {
        'Home Team':homeName2022,
        'Away Team':awayName2022
    }

    seasonGames2022 = pd.DataFrame(data2022)



    homeTeam2022 = []
    awayTeam2022 = []
    homePred2022 = []
    awayPred2022 = []
    for index, row in seasonGames2022.iterrows():
        homeTeamPlaying = row['Home Team']
        awayTeamPlaying = row['Away Team']
        
        homeTeamStats = df.loc[df['Home Team'] == homeTeamPlaying]
        homeTeamStatsAvg = homeTeamStats.mean()
            
        awayTeamStats = df.loc[df['Away Team'] == awayTeamPlaying]
        awayTeamStatsAvg = awayTeamStats.mean()
        
        
        #USE HOME DATA VARS
        homeData =[]
        for i in home_list:
            homeData.append(homeTeamStatsAvg[i])
                # homeTeamStatsAvg['Home Pass Touchdowns'],
                # homeTeamStatsAvg['Home Total']

            
            
            #USE AWAY DATA VARS
        awayData =[]
        for j in away_list:
            awayData.append(awayTeamStatsAvg[j])
            
        homeVarsList = np.asarray([homeData])
        awayVarsList = np.asarray([awayData])
            
        homePrediction = homeModel.predict(homeVarsList)
        awayPrediction = awayModel.predict(awayVarsList)
        
        # print(row['Home Team'] + '' + str(homePrediction))
        # print(row['Away Team'] + '' + str(awayPrediction))
        
        
        homeTeam2022.append(row['Home Team'])
        awayTeam2022.append(row['Away Team'])
        homePred2022.append(homePrediction[0])
        awayPred2022.append(awayPrediction[0])


    seasonPred2022 = {
        'Home Team':homeTeam2022,
        'Away Team':awayTeam2022,
        'Home Pred':homePred2022,
        'Away Pred':awayPred2022
    }


    seasonPredResults2022 = pd.DataFrame(seasonPred2022)


    winner = []
    for index, row in seasonPredResults2022.iterrows():
        if row['Home Pred']>row['Away Pred']:
            winner.append(row['Home Team'])
        else:
            winner.append(row['Away Team'])

    loser = []
    for index, row in seasonPredResults2022.iterrows():
        if row['Home Pred']>row['Away Pred']:
            loser.append(row['Away Team'])
        else:
            loser.append(row['Home Team'])


    teams = seasonPredResults2022['Home Team'].unique()


    from collections import Counter
    homeWins = []
    homeWinsTeam = []
    for i in teams:
        homeWinsTeam.append(i)
        counts = Counter(winner)
        homeWins.append(counts[i])

    homeLosses = []
    homeLossesTeam = []
    for i in teams:
        homeLossesTeam.append(i)
        counts = Counter(loser)
        homeLosses.append(counts[i])





    recordWins2022Data = {
    'homeWinsTeam':homeWinsTeam,
    'homeWins':homeWins
    }


    recordWins2022 = pd.DataFrame(recordWins2022Data)


    recordLosses2022Data = {
    'homeLossesTeam':homeLossesTeam,
    'homeLosses':homeLosses
    }


    recordLosses2022 = pd.DataFrame(recordLosses2022Data)



    records2022Pred = recordWins2022.merge(recordLosses2022, left_on='homeWinsTeam',right_on='homeLossesTeam')



    records2022Pred = records2022Pred.drop('homeLossesTeam',axis=1)


    records2022Pred.columns = ['Team','Wins','Losses']



    z=records2022Pred.sort_values(by='Wins',ascending=False)
    final_simulation=z.to_dict() 
    team=final_simulation["Team"]
    wins=final_simulation["Wins"]
    loss=final_simulation["Losses"]
    team_list=list(team.values())
    wins_list=list(wins.values())
    loss_list=list(loss.values())
    
    
    data={
        "status":"ok",
        "gameinfo":gameinfo,
        "team_stats": predict_list,
        "simulation":team_list,
        "wins":wins_list,
        "loss":loss_list
       

    }
    return JsonResponse(data)

           
def download_file(request):
    filename = "totalcsv/variableStats.csv"
    download_name ="variableStats.csv"
    with open(filename, 'r') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response


def download_corr_file(request):
    filename = "totalcsv/correlation.csv"
    download_name ="correlation.csv"
    with open(filename, 'r') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response



def deletemodel(request,id):
    var_get=Modelvar.objects.filter(modelname_id=id)
    
    var_del = Modelname.objects.get(id=id)
    var_del.delete()
    var_get.delete()

    return redirect('mymodel')


def selectvariable(request):
    return render(request,"signup/buildmodel3.html")


def training(request):
    return render(request,"signup/buildmodel4.html")

def modelname(request):
    two = Modelname.objects.all()
    if request.method == "POST":
        name = Modelname()  
        name.modelname = request.POST.get("modelname")
        name.user_id=request.user.id
        len_model=Modelname.objects.filter(user_id=request.user.id)
        name.save() 
        name1 = Modelvar.objects.filter(modelname_id__startswith ='f').update(modelname_id=name.id,status =1)
    
        return redirect('mymodel')
   
    return render(request,"signup/buildmodel5.html",{'two':two})

def mymodel(request):
    val=Modelname.objects.filter(user_id=request.user.id)
    print(val)
    if val:
        print("value")
    else:
        return render(request,"signup/mymodel.html")

    return render(request,"signup/mymodel.html",{"model_name":val})

def update(request,id):
  
    all1=Modelvar.objects.filter(modelname_id=id)
    print("Show",all1)
    req = request.GET .get('cars') 
    # print(newdata.query)
   
    st = StripeCustomer.objects.filter(stripeCustomerId = request.user.id).values_list("membershipstatus",flat=True)
    membership=list(st)
    
    if 1 in membership:
            
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
        df = pd.read_csv('totalcsv/finalDS1.csv')
        co = len(df.columns)

    


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
            "QB Yds Per Scram"]


        


        #getting shape. We will use this for back testing / training
        amountOfGames = df.shape[0]
     




        
    else:
        return redirect('membership') 


    return render(request,"signup/update.html",{'re':req,"df":list(df_away),"all":all1,"amount":amountOfGames,'id':id})





# def send_file(request):
#     img = open('resul.png', 'rb')
#     dow="h.png" 
#     response = HttpResponse(img)
#     response['Content-Disposition'] = 'attachment; filename=%s.png' %dow 

#     return response

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
                # print("////////////////////////",hriti[j].sort_values(ascending=False)[:10])
                top_ten=hriti[j].sort_values(ascending=False)[:10]
                # print("toppppp_tennnnn",top_ten)


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
            df = pd.read_csv('totalcsv/finalDS1.csv')
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
            describe=df.describe()
            corr= df.corr()
            corr.to_csv('totalcsv//correlation.csv')
            describe.to_csv('totalcsv//variableStats.csv')


    else:
        return redirect('membership') 
    return render(request,"signup/buildmodel1.html",{'re':req,"df":list(df_away),"all":all,"amount":amountOfGames})

def minmax(request):
    
    req = request.POST.getlist('minvalue[]')
    print("ss",req)
    df = pd.read_csv('totalcsv/finalDS1.csv')

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

