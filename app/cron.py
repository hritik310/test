
from pysbr import *
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time

	
from crontab import CronTab


from django.core.mail import send_mail as sm
	

import os
import tweepy as tw
import numpy as np
import matplotlib.pyplot as plt


# In[117]:
def today():
    df = pd.read_csv('/home/ubuntu/datasport/totalcsv/finalDS1.csv') 
    df = df[(df.Season == 2021)] 
    df=df[['IndexRow',"Home Team","Away Team","Home Total","Away Total"]].sort_values(by='IndexRow').dropna()
    

    # In[118]:

        
    def expected_result(loc,aw):
        dr=loc-aw
        we=(1/(10**(-dr/400)+1))
        return [np.round(we,3),1-np.round(we,3)]

    def actual_result(loc,aw):
        if loc<aw:
            wa=1
            wl=0
        elif loc>aw:
            wa=0
            wl=1
        elif loc==aw:
            wa=0.5
            wl=0.5
        return [wl,wa]

    def calculate_elo(elo_l,elo_v,local_goals,away_goals):
        
        wl,wv=actual_result(local_goals,away_goals)
        wel,wev=expected_result(elo_l,elo_v)

        elo_ln=elo_l+(wl-wel)
        elo_vn=elo_v+(wv-wev)

        return elo_ln,elo_vn


    # In[119]:


    current_elo={}
    for idx,row in df.iterrows():
        
        local=row['Home Team']
        away=row['Away Team']
        local_goals=row['Home Total']
        away_goals=row['Away Total']
        

        if local not in current_elo.keys():
            current_elo[local]=1300
        
        if away not in current_elo.keys():
            current_elo[away]=1300
        
        elo_l=current_elo[local]
        elo_v=current_elo[away]
        elo_ln,elo_vn=calculate_elo(elo_l,elo_v,local_goals,away_goals)

        current_elo[local]=elo_ln
        current_elo[away]=elo_vn
        
        df.loc[idx,'Elo_h_after']=elo_ln
        df.loc[idx,'Elo_a_after']=elo_vn 
        df.loc[idx,'Elo_h_before']=elo_l
        df.loc[idx,'Elo_a_before']=elo_v


    # In[120]:


    elos=df[['IndexRow','Home Team','Elo_h_after']].rename(columns={'Home Team':'Team','Elo_h_after':'Elo'}).append(df[['IndexRow','Away Team','Elo_a_after']].rename(columns={'Away Team':'Team','Elo_a_after':'Elo'}))


    # In[121]:


    elos


    # In[122]:


    team = []
    elo = []
    for i in elos['Team'].unique():
        teamElos = elos
        teamElos = teamElos[(teamElos.Team == i)] 
        lastOccurence = teamElos.iloc[-1]
        team.append(lastOccurence['Team'])
        elo.append(lastOccurence['Elo'])


    # In[123]:


    data = {
        'Team':team,
        'Elo Rating':elo
    }


    # In[124]:


    eloDF = pd.DataFrame(data)


    # In[125]:


    eloDF = eloDF.sort_values(by='Elo Rating', ascending=False)


    # In[127]:

     
    eloDF.to_csv('/home/ubuntu/datasport/totalcsv/eloDF.csv',index=False)

    # for local  
    # eloDF.to_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/eloDF.csv',index=False)
def gettoday():
    consumer_key= 'pAxYcP5JuHjBo3VSkn6QGbHSl'
    consumer_secret= 'oDlgo6qv7u5eO7pm2LRAJuXjMyaPby9VQbp26yaGdURwd80Y12'
    access_token= '501526851-tOWJUjhLNou2v7nJ6tsAOSTzOxTvIIRaPjl3MUrq'
    access_token_secret= 'ifF4ZbnGoSChzO6Nv5NzHackcHAzCcOvDqkdtKR7oZ7dD'



    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True,timeout=5)



    from datetime import datetime, timedelta
    yesterday = datetime.now() - timedelta(1)

    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')




    teams = ['Tampa Bay Buccaneers', 'Atlanta Falcons', 'Buffalo Bills',
    'Carolina Panthers', 'Cincinnati Bengals', 'Indianapolis Colts',
    'Tennessee Titans', 'Detroit Lions', 'Houston Texans',
    'Washington Commanders', 'Kansas City Chiefs',
    'New York Giants', 'New Orleans Saints', 'New England Patriots',
    'Los Angeles Rams', 'Las Vegas Raiders', 'Miami Dolphins',
    'Chicago Bears', 'Cleveland Browns', 'Jacksonville Jaguars',
    'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers',
    'Arizona Cardinals', 'Los Angeles Chargers', 'Seattle Seahawks',
    'Baltimore Ravens', 'Green Bay Packers', 'Denver Broncos',
    'Minnesota Vikings', 'San Francisco 49ers', 'Dallas Cowboys']

    teamTweets = []
    tweetSize = []
    for i in teams:
        print(i)
        new_search = i

        tweets = tw.Cursor(api.search_tweets,
        q=new_search,
        lang="en",
        since=yesterday).items(99999) #date can be changed

        all_tweets = [tweet.text for tweet in tweets]
        data = pd.DataFrame(data=all_tweets, columns=['Tweets'])
        data.to_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/'+i+'.csv')
        tweetSize.append(data.size)
        teamTweets.append(i)



    tweetDF = {
        'team':teamTweets,
        'tweet count':tweetSize
    }

    pd.DataFrame(tweetDF).to_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/tweetCount.csv',index=False)




