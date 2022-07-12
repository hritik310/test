
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
            # man=df[df.columns[1:]].corr()['home_steals'].sort_values(ascending=False)[:10]
            # print(man)
        #     df_columns = df[["home_steal_percentage",
        # "home_steals",
        # "home_three_point_attempt_rate",
        # "home_three_point_field_goal_attempts",
        # "home_three_point_field_goal_percentage",
        # "home_three_point_field_goals",
        # "home_total_rebound_percentage",
        # "home_total_rebounds",
        # "home_true_shooting_percentage",
        # "home_turnover_percentage",
        # "home_turnovers",
        # "home_two_point_field_goal_attempts",
        # "home_two_point_field_goal_percentage",
        # "home_two_point_field_goals",
        # "home_wins"]]
            # dfw = df.corr()
            # dataplot = sb.heatmap(df_columns.corr(), cmap="YlGnBu", annot=True)
            # dataplot.figure.savefig('resul.png')
            # # for j in answers_list:
               
            #     print(hrit[j].sort_values(ascending=False)[:10])
            # hrit.to_csv("/home/codenomad/Documents/GitHub/datasport/totalcsv/output.csv")
            # )
  
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
            # start=df.loc[df['season'] == 2018]
            # print(len(start))
            # Start = '2018'
            # df['season'] = pd(df['season'])
            # mask = (df['season']== Start)
            # use1 = len(df.loc[mask])

            # print ("hello0",use1)

        


            #getting shape. We will use this for back testing / training
            amountOfGames = df.shape[0]
            print("dgdg",amountOfGames)




        
    else:
        return redirect('membership') 


    return render(request,"signup/buildmodel.html",{'re':req,"df":list(df_away),"all":all,"amount":amountOfGames})
    # return render(request,"signup/buildmodel.html",{'H':data"df":list(df_away),'status':status,"all":all})
   

# def buildmodelStatus(request):
#     build = Var()
#     select = Selectvar()
#     build.created_by = request.user.id
#     good = Var.objects.filter(created_by= request.user.id)
#     print("good",good.query)
#     if good == 1:
#         build.save()
#     select.percent_value =request.GET.get('info')
#     select.title=request.GET.get('id')
  
#     print("build",select.title)

#     if  select.percent_value == "":
#         select.percent_value=0
#     select.save()
#     # dele=Modelvar.objects.all()
#     # dele.delete()  
#     data = {
#     "status":"OK",
#     "messages":"You have selected the item",
#     "message":"You have Selected the item",
#     "value":0,
#     }

#     return JsonResponse(data)
def buildmodelStatus(request):
    build = Modelvar()
    build.title=request.GET.get('id')
    print("build",build.title)
    build.created_by = request.user.id
    # build.percent_value =request.GET.get('info')
    # if  build.percent_value == "":
    #     build.percent_value=0
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

# def buildmodelpercent(request):

#     buil = Modelvar()
    
#     buil.percent_value = request.GET.get('id')
#     buil.save()
#     data = {
#     "status":"OK",
#     }

#     return JsonResponse(data)




def buildmodelbutton(request):

    reqs = request.GET.get('id',None)
    print(request.GET)
    if reqs == 'ncaab':
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
        df_away = df[['joinValue', 'over_under_total',
               'spreadtotal', 
               'participantscore', 'participant', 'participantfullname',
               'underdogscore', 'underdogteam', 'underdogabb', 'home', 'away',
               'dateForJoin', 'links', 
               'homeTeam', 'awayTeam', 'homeRank', 'awayRank', 'homeScore',
               'awayScore', 'awayMP', 'awayFG', 'awayFGA', 'awayFGperc', 'away2P',
               'away2PA', 'away2Pperc', 'away3P', 'away3PA', 'away3Pperc', 'awayFT',
               'awayFTA', 'awayFTperc', 'awayORB', 'awayDRB', 'awayTRB', 'awayAST',
               'awaySTL', 'awayBLK', 'awayTOV', 'awayPF', 'awayPTS', 'homeMP',
               'homeFG', 'homeFGA', 'homeFGperc', 'home2P', 'home2PA', 'home2Pperc',
               'home3P', 'home3PA', 'home3Pperc', 'homeFT', 'homeFTA', 'homeFTperc',
               'homeORB', 'homeDRB', 'homeTRB', 'homeAST', 'homeSTL', 'homeBLK',
               'homeTOV', 'homePF', 'homePTS', 'num']]
        


        # In[23]:


        #getting shape. We will use this for back testing / training
        amountOfGames = df.shape[0]
        print(amountOfGames)


        # In[24]:


        df


        # In[26]:


        df['actual_total_points'] = df['homePTS'] + df['awayPTS']


        # In[27]:


        df.columns


        # In[29]:


        backTest = [10,25,50,100,150]
        mode = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)
        carlen = len(mode)

        ans_list = list(mode)
        # print(answers_list)

        # for i in range(carlen,12):
        #     ans_list.append("num")
        # print(ans_list)
      
        total_list=[]
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

            ml_wins = 0
            ml_losses = 0
            
            #as a user selects and drops a variable it will be added and dropped 
            # to this list. This list is the list of variables used in the model
            # if len(ans_list)==12:
            #     modelVars=ans_list
            #     print(modelVars)
            modelVars=ans_list 
            # modelVars=['num',
            # 'homeFGperc',
            #    'homeFTperc',
            #   'homeORB',
            #  'homeTRB',
            # 'away2Pperc',
            # 'awayBLK',
            #    'awayFTA',
            #   'awayFTperc',
            #     'away3P']
            
            #we build two models but kind of use them just as one. We have the same
            #variables in both just a different target variable
            X = np.asarray(training[modelVars])
            Y_home=np.asarray(training['homePTS'])
            Y_away=np.asarray(training['awayPTS'])
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
                king=Modelvar.objects.filter(created_by=request.user.id).values_list("percent_value",flat=True)
                for nt in king:
                    print(nt)
                row2 = []
                for val in ans_list:
                    if val.startswith("away"):
                        averageValue = awayTeamAverages[val]
                        print(averageValue)
                        if king:
                            averageValue = (averageValue + (averageValue*nt/100))
 
                        row2.append(averageValue)

                    else:
                        averageValue = homeTeamAverages[val]
                        if king:
                            averageValue = (averageValue + (averageValue*nt)/100)

                        row2.append(averageValue)
                print("row2",row2)
                       
            
                new_data = asarray([row2])
                home_points = home_model.predict(new_data)[0]
                away_points = away_model.predict(new_data)[0]
   
                prediction_total_points = home_points + away_points

                if home_points > away_points and row['homePTS']>row['awayPTS']:
                    ml_wins = ml_wins + 1
                elif home_points > away_points and row['homePTS']<row['awayPTS']:
                    ml_losses = ml_losses + 1
                
                if away_points > home_points and row['awayPTS']>row['homePTS']:
                    ml_wins = ml_wins + 1
                elif away_points > home_points and row['awayPTS']<row['homePTS']:
                    ml_losses = ml_losses + 1
                



            
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
                if home == row['participantfullname']:
                   
            
            
                    point_diff = home_points-away_points
                 

            
                    if point_diff > abs(row['spreadtotal']):
                        if row['participantscore']-row['underdogscore']>abs(row['spreadtotal']):
                             wins = wins + 1
                        elif row['participantscore']-row['underdogscore']==abs(row['spreadtotal']):
                            ties = ties + 1

                        else:
                            losses = losses + 1


                       
                
                    if point_diff < abs(row['spreadtotal']):
                        if row['participantscore']-row['underdogscore']<abs(row['spreadtotal']):
                            wins = wins + 1
                    
                        elif row['participantscore']-row['underdogscore']==abs(row['spreadtotal']):
                            ties = ties + 1
                            
                        else:                
                            losses = losses + 1


                    
            
                    
                if away == row['participantfullname']:
                    
                    
                    point_diff = home_points-away_points
                    
                    if point_diff > abs(row['spreadtotal']):
                        if row['participantscore']-row['underdogscore']>row['spreadtotal']:
                            wins = wins + 1
                               
                            
                            
                            
                        elif row['participantscore']-row['underdogscore']==row['spreadtotal']:
                            ties = ties + 1
                        
                        
                        else:
                            losses = losses + 1


                            
                            
                    if point_diff < abs(row['spreadtotal']):
                        if row['participantscore']-row['underdogscore']<abs(row['spreadtotal']):
                            wins = wins + 1
                            
                       
                        elif row['participantscore']-row['underdogscore']==abs(row['spreadtotal']):
                            ties = ties + 1

                        else:
                            losses = losses + 1
            
            # print('Last ' + str(abs(i)) + ' games')
            # print('wins ML: ' + str(ml_wins))
            # print('losses ML: ' + str(ml_losses))
            # print('win% over/under: ' + str(ml_wins/(ml_wins + ml_losses)))
            # print('             ') 
            
            # print('Last ' + str(abs(i)) + ' games')
            # print('wins over/under: ' + str(total_wins))
            # print('losses over/under: ' + str(total_losses))
            # print('ties over/under: ' + str(total_ties))
            # games = abs(i)-total_ties
            # print('win% over/under: ' + str(total_wins/games))
            # print('             ')               
                            
            # print('Last ' + str(abs(i)) + ' games')
            # print('wins spread: ' + str(wins))
            # print('losses spread: ' + str(losses))
            # print('ties spread: ' + str(ties))
            # games = abs(i)-ties
            # print('win% spread: ' + str(wins/games))
            # print('             ')

            last = 'Last ' + str(abs(i)) + ' games'
            print('last',last)
            wi =str(ml_wins)
            print("wins",wi)
            lo =str(ml_losses)
            print("loss",lo)
            winover = 'win% over/under: ' + str(ml_wins/(ml_wins + ml_losses))
            print('winover',winover)

            lastgame='Last ' + str(abs(i)) + ' games'
            winoverunder = str(total_wins)
            lossoverunder = str(total_losses)
            tiesoverunder = str(total_ties)
            l=total_wins/(total_wins + total_losses+total_ties)
            percent_over = "{:.0%}".format(l)
            games = abs(i)-total_ties
            winpercent ='win% over/under: ' + str(total_wins/games) 

            lastt ='Last ' + str(abs(i)) + ' games'
            winspread = str(wins)
            lossspread = str(losses)
            tiesspread =  str(ties)
            q=wins/(wins+losses+ties)
            percent_spread= "{:.0%}".format(q)
            games = abs(i)-ties
            winpercentspread ='win% spread: ' + str(wins/games)
            data = {
                        'last_games':last,
                        'wins':wi,
                        'loss':lo,
                        'winover':winover,
                        'winoverunder':winoverunder,
                        'lossoverunder':lossoverunder,
                        'tiesoverunder':tiesoverunder,
                        'overunder_percent':percent_over,
                        'winspread':winspread,
                        'lossspread':lossspread,
                        'tiesspread':tiesspread,
                        'spread_percent':percent_spread,

                        
                    }

            total_list.append(data) 

            print(total_list) 






        # In[ ]:





        # In[30]:


        #get today


        # In[34]:


        # ncaab = NCAAB()
        # sb = Sportsbook()
        # cols = ['event', 'participant', 'spread / total', 'decimal odds', 'american odds']


        # # In[35]:


        # today= datetime.today()
        # year = today.year
        # month = today.month
        # day = today.day


        # # In[36]:


        # today = str(year) + '-' + str(month) + '-' + str(day)


        # # In[38]:


        # dt = datetime.strptime(today, '%Y-%m-%d')
        # e = EventsByDate(ncaab.league_id, dt)
        # spread = CurrentLines(e.ids(), ncaab.market_ids('pointspread'), sb.ids('Bovada')[0])
        # spread = spread.dataframe(e)


        # # In[39]:


        # favSpread = spread.loc[spread['spread / total'] <0]
        # undSpread = spread.loc[spread['spread / total'] >0]


        # # In[40]:
        # favSpread = favSpread.drop_duplicates(subset='event', keep='last')
        # undSpread = undSpread.drop_duplicates(subset='event', keep='last')


        # #get underdog score,team, and abbreviation 
        # undTeam = []
        # undAbb = []
        # ncaab_list = []
        # for index, row in undSpread.iterrows():
        #     undTeam.append(row['participant full name'])
        #     undAbb.append(row['participant'])


        # # In[41]:


        # favSpread['underdog team'] = undTeam
        # favSpread['underdog abb'] = undAbb


        # # In[42]:


        # filtered_spread = favSpread


        # # In[43]:


        # #find home and away teams

        # home = []
        # away = []

        # for index, row in filtered_spread.iterrows():
        #     findIndex = row['event'].find('@')
        #     home.append(row['event'][findIndex+1:])
        #     away.append(row['event'][:findIndex])
        # filtered_spread['home'] = home
        # filtered_spread['away'] = away


        # # In[46]:


        # filtered_spread=filtered_spread.drop_duplicates(subset=['event id'], keep='last')


        # # In[48]:


        # for index, row in filtered_spread.iterrows():
        #     homeTeam = df.loc[df['home']==row['home']]
        #     awayTeam = df.loc[df['away']==row['away']]

            
        #     homeTeamAverages = homeTeam.mean()
        #     awayTeamAverages = awayTeam.mean()
            
            
            
        #     pred = []
        #     for values in ans_list:
        #         if values.startswith("away"):
        #             pred.append(awayTeamAverages[values])
        #         else:
        #             pred.append(homeTeamAverages[values])
                       
            
            
            
            
        #     new_data = asarray([pred])
        #     home_points = round(home_model.predict(new_data)[0],1)
        #     away_points = round(away_model.predict(new_data)[0],1)

        #     if home_points > 50 and away_points>50:
        #         print(row['home'] + ' vs ' + row['away'])
        #         print('Prediction')
        #         homerow = row['home'] + ' ' + str(home_points) + ' vs ' + row['away'] + ' ' + str(away_points)
        #         awayrow=row['away'] + ' ' + str(away_points)
        #         data ={

        #             'home':homerow,
        #             'away':awayrow,

        #         }
        #         ncaab_list.append(data)
        #         print(ncaab_list)

        data1 = {
        "status":"OK",
        "data":reqs,
        "total":total_list,
        # "ncaab":ncaab_list,
        "win":wi,
        "loss":lo,

        }




    
    else:
        df = pd.read_csv('totalcsv/finalDS.csv')

        # df = df.dropna()

        # df = df.replace(to_replace ="New Orleans",value ="New Orleans Pelicans")
        # df = df.replace(to_replace ="L.A. Clippers Clippers",value ="Los Angeles Clippers")
        # df = df.replace(to_replace ="L.A. Clippers",value ="Los Angeles Clippers")
        # df = df.replace(to_replace ="LA Clippers",value ="Los Angeles Clippers")
        # df = df.replace(to_replace ="Oklahoma City",value ="Oklahoma City Thunder")
        # df = df.replace(to_replace ="Golden State",value ="Golden State Warriors")
        # df = df.replace(to_replace ="New York",value ="New York Knicks")
        # df = df.replace(to_replace ="L.A. Lakers Lakers",value ="Los Angeles Lakers")
        # df = df.replace(to_replace ="LA Lakers",value ="Los Angeles Lakers")
        # df = df.replace(to_replace ="L.A. Lakers",value ="Los Angeles Lakers")
        # df = df.replace(to_replace ="San Antonio",value ="San Antonio Spurs")


        # df['num'] = 1
        # pert=df['americanodds'].max()
        # print("pert",pert)


        df = df[["Home Team",
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
    




        # df['actual_total_points'] = df['home_points'] + df['away_points']


        # In[117]:


        backTest = [10,25,50,100]
        var = Modelvar.objects.filter(created_by = request.user.id).values_list("title",flat=True)

        car = len(var)

        answers_list = list(var)
        print("answer",answers_list)
        
        # print('answers_list',answers_list)

        # for i in range(car,12):
        #     answers_list.append("num")
        # print(answers_list)
      

     



        # data_list =[]
        
        # for i in backTest:
        #     training = df[:amountOfGames-i]
        #     print(training.shape)
        #     predictionGames = df[i*-1:]
        #     print(predictionGames.shape)
        #     wins = 0
        #     losses = 0
        #     ties = 0
            
        #     total_wins = 0
        #     total_losses = 0
        #     total_ties = 0
            
        #     ml_wins = 0
        #     ml_losses = 0
        #     #as a user selects and drops a variable it will be added and dropped 
        #     # to this list. This list is the list of variables used in the model
        #     # if len(answers_list)==12:
        #     #     modelVars=answers_list
        #     #     print(modelVars)
        #     modelVars = answers_list
             
        #     # else:
        #     #     modelVars=['num',
        #     #     'away_defensive_rating',    
        #     #     'away_offensive_rating',
        #     #     'away_three_point_attempt_rate',
        #     #     'away_true_shooting_percentage',
        #     #     'away_turnover_percentage',
        #     #     'home_defensive_rating',
        #     #     'home_offensive_rating',
        #     #     'home_three_point_attempt_rate',
        #     #     'home_true_shooting_percentage',
        #     #     'home_turnover_percentage',
        #     #     'pace']
        
        #     #we build two models but kind of use them just as one. We have the same
        #     #variables in both just a different target variable
        #     # X = np.asarray(training[modelVars])
        #     # Y_home=np.asarray(training['home_points'])
        #     # Y_away=np.asarray(training['away_points'])
        #     #fit the model for home_points and away_points

        #     home_model = xgb.XGBRegressor()
        #     away_model = xgb.XGBRegressor()
        #     feats = {}
        #     home_model.fit(X,Y_home)
        #     for feature, importance in zip(answers_list,home_model.feature_importances_):
        #         feats[feature] = str(round(importance*100))#add the name/value pair
        #     # print("featuer_importance_home_model",home_model.importance_type)

        #     weight= home_model.get_booster().get_score(importance_type='weight')
        #     a_dict = {key: value for key, value in zip(answers_list, weight.values())}

        #     total_gain = home_model.get_booster().get_score(importance_type='total_gain')
        #     a_total = {key: round(value,2) for key, value in zip(answers_list, total_gain.values())}
    

        #     cover = home_model.get_booster().get_score(importance_type='cover')
        #     a_cover = {key: round(value,2) for key, value in zip(answers_list, cover.values())}
            
 
        #     total_cover = home_model.get_booster().get_score(importance_type='total_cover')
        #     a_total_cover = {key: value for key, value in zip(answers_list, total_cover.values())}
            

        #     feats_feature = feats
        #     # print(feats_feature)

        #     away_model.fit(X,Y_away)
        #     # print("featuer_importance_away_model",away_model)
            
            
            
            
            
        #     for index, row in predictionGames.iterrows():
        #         home = row['home']
        #         away = row['away']
               

                
               
        #         homeTeam = df.loc[df['home']==home]
    
        #         awayTeam = df.loc[df['away']==away]
             
        #         #get the averages of the playing
        #         #we use averages to make predictions
        #         homeTeamAverages = homeTeam.mean()
        #         awayTeamAverages = awayTeam.mean()
                
        #         #NEED HELP HERE
        #         #so the user adds the variables into the list modelVars
        #         #but I am not sure how we can dynamically use that list to 
        #         #select them from the averages dataframe we create.
        #         king=Modelvar.objects.filter(created_by=request.user.id).values_list("percent_value",flat=True)
        #         for nt in king:
        #             pass
                
            
              
                
        #         # avgfg=dpanda*rere/100 
        #         # tt=dpanda+avgfg
        #         # showt=list(tt)
        #         # print("showt",showt)
        #         row2=[]    
        #         for val in answers_list:
        #             if val.startswith("away"):
        #                 averageValue = awayTeamAverages[val]
        #                 # print(averageValue)
        #                 if king:
        #                     averageValue = (averageValue + (averageValue*nt/100))

        #                 row2.append(averageValue)

        #             else:
        #                 averageValue = homeTeamAverages[val]
        #                 if king:
        #                     averageValue = (averageValue + (averageValue*nt)/100)

        #                 row2.append(averageValue)
                
        #         # print("row2",row2)


               
             
    
        #         new_data = asarray([row2])
        #         home_points = home_model.predict(new_data)[0]
              
        #         away_points = away_model.predict(new_data)[0]

        #         prediction_total_points = home_points + away_points
                 
        #         if home_points > away_points and row['home_points']>row['away_points']:
        #             ml_wins = ml_wins + 1
        #         elif home_points > away_points and row['home_points']<row['away_points']:
        #             ml_losses = ml_losses + 1

        #         if away_points > home_points and row['away_points']>row['home_points']:
        #             ml_wins = ml_wins + 1
        #         elif away_points > home_points and row['away_points']<row['home_points']:
        #             ml_losses = ml_losses + 1
               
                
                    
            
        #         if prediction_total_points>row['over_under_total']:
        #             if row['actual_total_points']>row['over_under_total']:
        #                 total_wins = total_wins + 1
        #             elif row['actual_total_points']==row['over_under_total']:
        #                 total_ties = total_ties + 1
        #             else:
        #                 total_losses = total_losses + 1
                
        #         if prediction_total_points<row['over_under_total']:
        #             if row['actual_total_points']<row['over_under_total']:
        #                 total_wins = total_wins + 1
        #             elif row['actual_total_points']==row['over_under_total']:
        #                 total_ties = total_ties + 1
        #             else:
        #                 total_losses = total_losses + 1
                
              
                
                
                
        #         #code to get the record for the model
        #         if home == row['participantfullname']:
                   
            
            
        #             point_diff = home_points-away_points
                 

            
        #             if point_diff > abs(row['spreadtotal']):
        #                 if row['participantscore']-row['underdogscore']>abs(row['spreadtotal']):
        #                      wins = wins + 1
        #                 elif row['participantscore']-row['underdogscore']==abs(row['spreadtotal']):
        #                     ties = ties + 1
                        
        #                 else:                
        #                     losses = losses + 1



                


                       
                
        #             if point_diff < abs(row['spreadtotal']):
        #                 if row['participantscore']-row['underdogscore']<abs(row['spreadtotal']):
        #                     wins = wins + 1
                    
        #                 elif row['participantscore']-row['underdogscore']==abs(row['spreadtotal']):
        #                     ties = ties + 1
                            
        #                 else:                
        #                     losses = losses + 1


                    
            
                    
        #         if away == row['participantfullname']:
                    
                    
        #             point_diff = home_points-away_points
                    
        #             if point_diff > abs(row['spreadtotal']):
        #                 if row['participantscore']-row['underdogscore']>row['spreadtotal']:
        #                     wins = wins + 1
                               
                            
                            
                            
        #                 elif row['participantscore']-row['underdogscore']==row['spreadtotal']:
        #                     ties = ties + 1
                        
                        
        #                 else:
        #                     losses = losses + 1


                            
                            
        #             if point_diff < abs(row['spreadtotal']):
        #                 if row['participantscore']-row['underdogscore']<abs(row['spreadtotal']):
        #                     wins = wins + 1
                            
                       
        #                 elif row['participantscore']-row['underdogscore']==abs(row['spreadtotal']):
        #                     ties = ties + 1

        #                 else:
        #                     losses = losses + 1



        #     nba = NBA()
        #     sb = Sportsbook()
        #     cols = ['event', 'participant', 'spread / total', 'decimal odds', 'american odds']


        #     # In[132]:


        #     today= datetime.today()
        #     year = today.year
        #     month = today.month
        #     day = today.day


        #     # In[133]:


        #     today = str(year) + '-' + str(month) + '-' + str(day)


        #     # In[134]:


        #     dt = datetime.strptime(today, '%Y-%m-%d')
        #     et = EventsByDate(nba.league_id, dt)
        #     spread = CurrentLines(et.ids(), nba.market_ids('pointspread'), sb.ids('Bovada')[0])
        #     spread = spread.dataframe(et)


        #     # In[135]:


        #     favSpread = spread.loc[spread['spread / total'] <0]
        #     undSpread = spread.loc[spread['spread / total'] >0]


        #     # In[136]:


        #     #get underdog score,team, and abbreviation 
        #     undTeam = []
        #     undAbb = []
        #     another_list=[]
        #     for index, row in undSpread.iterrows():
        #         undTeam.append(row['participant full name'])
        #         undAbb.append(row['participant'])


        #     # In[137]:


        #     favSpread['underdog team'] = undTeam
        #     favSpread['underdog abb'] = undAbb


        #     # In[138]:


        #     filtered_spread = favSpread


        #     # In[143]:


        #     #find home and away teams

        #     home = []
        #     away = []

        #     for index, row in filtered_spread.iterrows():
        #         findIndex = row['event'].find('@')
        #         home.append(row['event'][findIndex+1:])
        #         away.append(row['event'][:findIndex])
        #     filtered_spread['home'] = home
        #     filtered_spread['away'] = away


        #     # In[144]:


        #     #preprocessing to match up names
        #     filtered_spread = filtered_spread.replace(to_replace ="New Orleans",value ="New Orleans Pelicans")
        #     filtered_spread = filtered_spread.replace(to_replace ="L.A. Clippers Clippers",value ="Los Angeles Clippers")
        #     filtered_spread = filtered_spread.replace(to_replace ="LA Clippers",value ="Los Angeles Clippers")
        #     filtered_spread = filtered_spread.replace(to_replace ="Oklahoma City",value ="Oklahoma City Thunder")
        #     filtered_spread = filtered_spread.replace(to_replace ="Golden State",value ="Golden State Warriors")
        #     filtered_spread = filtered_spread.replace(to_replace ="New York",value ="New York Knicks")
        #     filtered_spread = filtered_spread.replace(to_replace ="L.A. Lakers Lakers",value ="Los Angeles Lakers")
        #     filtered_spread = filtered_spread.replace(to_replace ="LA Lakers",value ="Los Angeles Lakers")
        #     filtered_spread = filtered_spread.replace(to_replace ="L.A. Lakers",value ="Los Angeles Lakers")
        #     filtered_spread = filtered_spread.replace(to_replace ="San Antonio",value ="San Antonio Spurs")


        #     # In[146]:


        #     for index, row in filtered_spread.iterrows():
        #         homeTeam = df.loc[df['home']==row['home']]
        #         awayTeam = df.loc[df['away']==row['away']]

                
        #         homeTeamAverages = homeTeam.mean()
        #         awayTeamAverages = awayTeam.mean()


        #         # print(row['home'] + ' vs ' + row['away'])
                
        #         pred = []
        #         for value in answers_list:
        #             if value.startswith("away"):
        #                 pred.append(awayTeamAverages[value])
        #             else:
        #                 pred.append(homeTeamAverages[value])
                
                
                
        #         new_data = asarray([pred])
        #         home_points = round(home_model.predict(new_data)[0],1)
        #         away_points = round(away_model.predict(new_data)[0],1)

                
        #         print('Prediction')
        #         print(row['home'] + ' ' + str(home_points))
        #         print(row['away'] + ' ' + str(away_points))

        #         hme=row['home'] + ' ' + str(home_points) + '  vs  ' + row['away'] + ' ' + str(away_points)
        #         awy=row['away'] + ' ' + str(away_points)
        #         datar={

        #         'home':hme,
        #         'away':awy,
        #         }
        #         another_list.append(datar) 
        #     # print(another_list)   
        #     y='Last '+str(abs(i))
        #     w=str(ml_wins)
        #     e=str(ml_losses)
        #     r=ml_wins/(ml_wins + ml_losses)
        #     percentage = "{:.0%}".format(r)

            
        #     h='Last ' + str(abs(i))
        #     j=total_wins
        #     k=str(total_losses)
        #     pri = str(total_ties)
        #     l=j/(total_wins + total_losses+total_ties)
        #     percent_over = "{:.0%}".format(l)
        #     games = abs(i)-total_ties
        #     m='win% over/under: ' + str(total_wins/games)
        #     print('             ')               
                            
        #     n='Last ' + str(abs(i)) + 'games'
        #     o=wins
        #     p=str(losses)
        #     spread_tie = str(ties)
        #     q=o/(wins+losses)
        #     percent_spread= "{:.0%}".format(q)
        #     games = abs(i)-ties
        #     s='win% spread: ' + str(wins/games)



        #     data = {
        #                 'last_games':h,
        #                 'wins':j,
        #                 'loss':k,
        #                 'ties':pri,
        #                 'percent':percent_over,
        #                 'ML_last_games':y,
        #                 'ML_wins':w,
        #                 'ML_loss':e,
        #                 'ML_ties':percentage,
        #                 "spread_last_games":n,
        #                 "spread_wins":o,
        #                 'spread_loss':p,
        #                 'spread_ties':spread_tie,
        #                 'spread_percent':percent_spread,
        #                 'home':hme,
                        
        #             }

        #     data_list.append(data)

            # print(data_list) 
      
        data1 = {
        "status":"OK",
        # "data":reqs,
        # "total":data_list,
        # "totalagain":another_list,
        # 'feature':feats,
        # "win":j,
        # "loss":k,
        # 'ties':pri,
        # "percent":percent_over,
        # 'ML_last_games':y,
        # 'ML_wins':w,
        # 'ML_loss':e,
        # 'ML_ties':percentage,
        # "spread_last_games":n,
        # "spread_wins":o,
        # 'spread_loss':p,
        # 'spread_ties':spread_tie,
        # 'spread_percent':percent_spread,
        # 'home':hme,
        # 'weight':a_dict,
        # 'total_gain':a_total,
        # 'cover':a_cover,
        # 'total_cover':a_total_cover,
        
        }

        # subject, from_email, to = 'hello', 'testsood981@gmail.com', request.user.email
        # text_content = 'This is an important message.'
        # html_content = render_to_string('signup/email.html',{'y':data_list})
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()


    # mod = Modelvar.objects.all().delete()

    return JsonResponse(data1)


def download_file(request):
    filename = "totalcsv/output.csv"
    download_name ="example.csv"
    with open(filename, 'r') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response




def reset(request):
    del_model=Modelvar.objects.all().delete()

    return redirect("/buildmodel")

def new(request):
    return render(request,"signup/new.html")

# def heatmap(request):
#     return render(request,"signup/buildmodel1.html")



# def selectml(request):
#     return render(request,"signup/buildmodel2.html")

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
         newlist=1088

    data = {
    "status":"OK",
    "dataset":newlist
    }
    return JsonResponse(data)

def value_select(request):     
    df = pd.read_csv('totalcsv/finalDS.csv')
    value_in=[]
    home_list=[]
    away_list=[]
    df_col=df.columns
    value1=request.GET.getlist("id[]")
  
    # print(value1)
    for z in value1:
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
