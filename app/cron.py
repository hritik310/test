
from pysbr import *
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time

	
from crontab import CronTab


from django.core.mail import send_mail as sm
	
import tweepy as tw
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import textblob
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,classification_report
from sklearn.metrics import plot_confusion_matrix


import os
directory = os.getcwd()


# In[117]:
def today():
    df = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/finalDS1.csv') 
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

     
    eloDF.to_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/eloDF.csv',index=False)

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

def Perctweets():
   
    tweetCount = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/tweetCount.csv')


    # In[165]:
    
    teams = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/teams.csv')


    # In[166]:


    lm = WordNetLemmatizer()

    def text_transformation(df_col):
        # res = sm(
        # subject = 'Subject here',
        # message = 'Hii there. I am in function',
        # from_email = 'testsood981@gmail.com',
        # recipient_list = ['hritik@codenomad.net'],
        # fail_silently=False,
        # )

        corpus = []
        for item in df_col:
            new_item = re.sub('[^a-zA-Z]',' ',str(item))
            new_item = new_item.lower()
            new_item = new_item.split()
            new_item = [lm.lemmatize(word) for word in new_item if word not in set(stopwords.words('english'))]
            corpus.append(' '.join(str(x) for x in new_item))
        return corpus

    def Average(lst):
        # res = sm(
        # subject = 'Subject here',
        # message = 'Hii there. I am in function average',
        # from_email = 'testsood981@gmail.com',
        # recipient_list = ['hritik@codenomad.net'],
        # fail_silently=False,
        # )
        return sum(lst) / len(lst)
    
    # Driver Code


    percentageList = []
    scoreList = []
    teamList = []
    for index,row in teams.iterrows():
        sentimentScores = []
        positiveTweetCounter = 0
        negativeTweetCounter = 0
        
        tweetScores = []
        
        i = 0
        df = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/'+row['Team']+'.csv')
        
        corpus = text_transformation(df['Tweets'])
        
        while i < len(corpus):
            try:
                blob = textblob.TextBlob(corpus[i])
                sentiment = blob.sentiment.polarity
            
                if sentiment >0:
                    sentimentScores.append(sentiment)
                    positiveTweetCounter = positiveTweetCounter + 1
                    tweetScores.append(sentiment)
                    
                if sentiment <0:
                    sentimentScores.append(sentiment)
                    negativeTweetCounter = negativeTweetCounter + 1
                    tweetScores.append(sentiment)
                
                i = i + 1
            except:
                print('failed tweet')
                i = i + 1
            
        teamList.append(row['Team'])
        percentageList.append(positiveTweetCounter/len(sentimentScores))
        scoreList.append(Average(tweetScores))
            
        


    # In[167]:


    sentimentDF = {
        'team':teamList,
        'percentage':percentageList,
        'scoreList':scoreList
    }

    sentimentDF = pd.DataFrame(sentimentDF)


    # In[168]:


    sentimentDF = sentimentDF.sort_values('percentage',ascending=False)


    # In[169]:


    from matplotlib import pyplot as plt
    


    # Plot bar chart with data points
    plt.bar(sentimentDF['team'], sentimentDF['percentage'])
    plt.xticks(rotation=90)
    plt.title("Percentage of tweets that are positive")
    plt.xlabel('Team') 
    plt.ylabel('Percentage %')
    filepath = '/home/codenomad/Documents/GitHub/datasport/app/static/image/plot1.png'
    if os.path.isfile(filepath):
        os.remove(filepath) 
    # plt.figure(figsize=(15,13))
    plt.tight_layout() 
    plt.savefig(filepath)
    plt.close()

def Plot2():
  


    tweetCount = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/tweetCount.csv')


    # In[165]:
    
    teams = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/teams.csv')


    # In[166]:


    lm = WordNetLemmatizer()

    def text_transformation(df_col):
        corpus = []
        for item in df_col:
            new_item = re.sub('[^a-zA-Z]',' ',str(item))
            new_item = new_item.lower()
            new_item = new_item.split()
            new_item = [lm.lemmatize(word) for word in new_item if word not in set(stopwords.words('english'))]
            corpus.append(' '.join(str(x) for x in new_item))
        return corpus

    def Average(lst):
        return sum(lst) / len(lst)
    
    # Driver Code


    percentageList = []
    scoreList = []
    teamList = []
    for index,row in teams.iterrows():
        sentimentScores = []
        positiveTweetCounter = 0
        negativeTweetCounter = 0
        
        tweetScores = []
        
        i = 0
        df = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/'+row['Team']+'.csv')
        
        corpus = text_transformation(df['Tweets'])
        
        while i < len(corpus):
            try:
                blob = textblob.TextBlob(corpus[i])
                sentiment = blob.sentiment.polarity
            
                if sentiment >0:
                    sentimentScores.append(sentiment)
                    positiveTweetCounter = positiveTweetCounter + 1
                    tweetScores.append(sentiment)
                    
                if sentiment <0:
                    sentimentScores.append(sentiment)
                    negativeTweetCounter = negativeTweetCounter + 1
                    tweetScores.append(sentiment)
                
                i = i + 1
            except:
                print('failed tweet')
                i = i + 1
            
        teamList.append(row['Team'])
        percentageList.append(positiveTweetCounter/len(sentimentScores))
        scoreList.append(Average(tweetScores))
            
        


    # In[167]:


    sentimentDF = {
        'team':teamList,
        'percentage':percentageList,
        'scoreList':scoreList
    }

    sentimentDF = pd.DataFrame(sentimentDF)


    # In[168]:


    sentimentDF = sentimentDF.sort_values('percentage',ascending=False)


    # In[169]:




   

    # In[170]:


    sentimentDF = sentimentDF.sort_values('scoreList',ascending=False)


    # # # In[171]:


    # # # Plot bar chart with data points
    plt.bar(sentimentDF['team'], sentimentDF['scoreList'])
    plt.xticks(rotation=90)
    plt.title("Avg score for every tweet -1(negative) to 1(positive)")
    plt.xlabel('Team') 
    plt.ylabel('Avg Sentiment Score') 
    filepath = '/home/codenomad/Documents/GitHub/datasport/app/static/image/plot2.png'
    if os.path.isfile(filepath):
        os.remove(filepath) 
    # plt.figure(figsize=(15,13)) 
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

def Plot3():


    tweetCount = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/tweetCount.csv')


    # In[165]:
    
    teams = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/teams.csv')


    # In[166]:


    lm = WordNetLemmatizer()

    def text_transformation(df_col):
        corpus = []
        for item in df_col:
            new_item = re.sub('[^a-zA-Z]',' ',str(item))
            new_item = new_item.lower()
            new_item = new_item.split()
            new_item = [lm.lemmatize(word) for word in new_item if word not in set(stopwords.words('english'))]
            corpus.append(' '.join(str(x) for x in new_item))
        return corpus

    def Average(lst):
        return sum(lst) / len(lst)
    
    # Driver Code


    percentageList = []
    scoreList = []
    teamList = []
    for index,row in teams.iterrows():
        sentimentScores = []
        positiveTweetCounter = 0
        negativeTweetCounter = 0
        
        tweetScores = []
        
        i = 0
        df = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/'+row['Team']+'.csv')
        
        corpus = text_transformation(df['Tweets'])
        
        while i < len(corpus):
            try:
                blob = textblob.TextBlob(corpus[i])
                sentiment = blob.sentiment.polarity
            
                if sentiment >0:
                    sentimentScores.append(sentiment)
                    positiveTweetCounter = positiveTweetCounter + 1
                    tweetScores.append(sentiment)
                    
                if sentiment <0:
                    sentimentScores.append(sentiment)
                    negativeTweetCounter = negativeTweetCounter + 1
                    tweetScores.append(sentiment)
                
                i = i + 1
            except:
                print('failed tweet')
                i = i + 1
            
        teamList.append(row['Team'])
        percentageList.append(positiveTweetCounter/len(sentimentScores))
        scoreList.append(Average(tweetScores))
            
        


    # In[167]:


    sentimentDF = {
        'team':teamList,
        'percentage':percentageList,
        'scoreList':scoreList
    }

    sentimentDF = pd.DataFrame(sentimentDF)


    # In[168]:


    sentimentDF = sentimentDF.sort_values('percentage',ascending=False)


    # In[169]:



    tweetCount = tweetCount.sort_values('tweet count',ascending=False)


    # # # In[173]:


    # # # Plot bar chart with data points
    plt.bar(tweetCount['team'], tweetCount['tweet count'])
    plt.xticks(rotation=90)
    plt.title("Tweet Traffic For Every Team")
    plt.xlabel('Team') 
    plt.ylabel('Tweets') 
    # Display the plot
    filepath = '/home/codenomad/Documents/GitHub/datasport/app/static/image/plot3.png'
    if os.path.isfile(filepath):
        os.remove(filepath) 
    # plt.figure(figsize=(15,13)) 
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
   





 



