#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Once select sport is selected on interface these snippits run


# In[15]:


#imports to run all of the code
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
from pysbr import *


# In[16]:


#read in csv file for development
#we can either read from s3 or have this data in the database
#regardless I have a few scripts that will update it daily
#we can decide later as this is just a sample dataset for testing


# In[17]:


df = pd.read_csv('mainDSNCAAB.csv')


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
df = df[['joinValue', 'over_under_total',
       'spread / total', 
       'participant score', 'participant', 'participant full name',
       'underdog score', 'underdog team', 'underdog abb', 'home', 'away',
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
    modelVars=['num',
    'homeFGperc',
       'homeFTperc',
      'homeORB',
     'homeTRB',
    'away2Pperc',
    'awayBLK',
       'awayFTA',
      'awayFTperc',
        'away3P']
    
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
        row2 = [1,
          homeTeamAverages['homeFGperc'],
          homeTeamAverages['homeFTperc'],
          homeTeamAverages['homeORB'],
          homeTeamAverages['homeTRB'],
          awayTeamAverages['away2Pperc'],
          awayTeamAverages['awayBLK'],
           awayTeamAverages['awayFTA'],
           awayTeamAverages['awayFTperc'],
           awayTeamAverages['away3P'],
               ]
    
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
    print('wins ML: ' + str(ml_wins))
    print('losses ML: ' + str(ml_losses))
    print('win% over/under: ' + str(ml_wins/(ml_wins + ml_losses)))
    print('             ') 
    
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


# In[ ]:





# In[30]:


#get today


# In[34]:


ncaab = NCAAB()
sb = Sportsbook()
cols = ['event', 'participant', 'spread / total', 'decimal odds', 'american odds']


# In[35]:


today= datetime.today()
year = today.year
month = today.month
day = today.day


# In[36]:


today = str(year) + '-' + str(month) + '-' + str(day)


# In[38]:


dt = datetime.strptime(today, '%Y-%m-%d')
e = EventsByDate(ncaab.league_id, dt)
spread = CurrentLines(e.ids(), ncaab.market_ids('pointspread'), sb.ids('Bovada')[0])
spread = spread.dataframe(e)


# In[39]:


favSpread = spread.loc[spread['spread / total'] <0]
undSpread = spread.loc[spread['spread / total'] >0]


# In[40]:
favSpread = favSpread.drop_duplicates(subset='event', keep='last')
undSpread = undSpread.drop_duplicates(subset='event', keep='last')


#get underdog score,team, and abbreviation 
undTeam = []
undAbb = []
for index, row in undSpread.iterrows():
    undTeam.append(row['participant full name'])
    undAbb.append(row['participant'])


# In[41]:


favSpread['underdog team'] = undTeam
favSpread['underdog abb'] = undAbb


# In[42]:


filtered_spread = favSpread


# In[43]:


#find home and away teams

home = []
away = []

for index, row in filtered_spread.iterrows():
    findIndex = row['event'].find('@')
    home.append(row['event'][findIndex+1:])
    away.append(row['event'][:findIndex])
filtered_spread['home'] = home
filtered_spread['away'] = away


# In[46]:


filtered_spread=filtered_spread.drop_duplicates(subset=['event id'], keep='last')


# In[48]:


for index, row in filtered_spread.iterrows():
    homeTeam = df.loc[df['home']==row['home']]
    awayTeam = df.loc[df['away']==row['away']]

    
    homeTeamAverages = homeTeam.mean()
    awayTeamAverages = awayTeam.mean()
    
    
    
    pred = [1,
          homeTeamAverages['homeFGperc'],
          homeTeamAverages['homeFTperc'],
          homeTeamAverages['homeORB'],
          homeTeamAverages['homeTRB'],
          awayTeamAverages['away2Pperc'],
          awayTeamAverages['awayBLK'],
           awayTeamAverages['awayFTA'],
           awayTeamAverages['awayFTperc'],
           awayTeamAverages['away3P'],
               ]
    
    
    
    
    new_data = asarray([pred])
    home_points = home_model.predict(new_data)[0]
    away_points = away_model.predict(new_data)[0]

    if home_points > 50 and away_points>50:
        print(row['home'] + ' vs ' + row['away'])
        print('Prediction')
        print(row['home'] + ' ' + str(home_points))
        print(row['away'] + ' ' + str(away_points))
    


# In[ ]:




