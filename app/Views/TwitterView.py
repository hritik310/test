#!/usr/bin/env python
# coding: utf-8

# In[163]:

from django.shortcuts import render
import pandas as pd
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
from django.http import JsonResponse
import time
import os
directory = os.getcwd()

# In[164]:

def tweetshow(request):
    return render(request,"twitter/tweets.html")
def Perctweets(request):
    print("enter")

    tweetCount = pd.read_csv('totalcsv/tweetCount.csv')


    # In[165]:
    
    teams = pd.read_csv('totalcsv/teams.csv')


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
        df = pd.read_csv('totalcsv/'+row['Team']+'.csv')
        
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
    filepath = directory + '/app/static/image/plot1.png'
    if os.path.isfile(filepath):
        os.remove(filepath) 
    # plt.figure(figsize=(15,13)) 
    plt.savefig(filepath)



    # directory = os.getcwd()
    # filepath = directory + '/app/static/image/plot1.png'
    # if os.path.isfile(filepath):
    #     os.remove(filepath) 
    # # plt.figure(figsize=(15,13)) 
    # plt.savefig(filepath)

    # Display the plot
    # plt.show()
    # plt.savefig(directory + '/app/static/image/plot1.png')
   

    # In[170]:


    # sentimentDF = sentimentDF.sort_values('scoreList',ascending=False)


    # # # In[171]:


    # # # Plot bar chart with data points
    # plt.bar(sentimentDF['team'], sentimentDF['scoreList'])
    # plt.xticks(rotation=90)
    # plt.title("Avg score for every tweet -1(negative) to 1(positive)")
    # plt.xlabel('Team') 
    # plt.ylabel('Avg Sentiment Score') 
    # aga = plt.show()
    # # # Display the plot
    # # # filepath = directory + '/app/static/image/plot2.png'
    # # # if os.path.isfile(filepath):
    # # #     os.remove(filepath)  
    # # # plt.savefig(filepath)



    # # # In[ ]:





    # # # In[172]:


    # tweetCount = tweetCount.sort_values('tweet count',ascending=False)


    # # # In[173]:


    # # # Plot bar chart with data points
    # plt.bar(tweetCount['team'], tweetCount['tweet count'])
    # plt.xticks(rotation=90)
    # plt.title("Tweet Traffic For Every Team")
    # plt.xlabel('Team') 
    # plt.ylabel('Tweets') 
    # # Display the plot
    # baga =plt.show()
    # # filepath = directory + '/app/static/image/plot3.png'
    # # if os.path.isfile(filepath):
    # #     os.remove(filepath)  
    # # plt.savefig(filepath)
    # return render(request,"twitter/tweets.html")

    
    # In[ ]:

    data = {
    "status":"OK",
    "data1":"/static/image/plot1.png",
    }

    return JsonResponse(data)



    # In[ ]:
def Plot2(request):

    tweetCount = pd.read_csv('totalcsv/tweetCount.csv')


    # In[165]:
    
    teams = pd.read_csv('totalcsv/teams.csv')


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
        df = pd.read_csv('totalcsv/'+row['Team']+'.csv')
        
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
    filepath = directory + '/app/static/image/plot2.png'
    if os.path.isfile(filepath):
        os.remove(filepath) 
    # plt.figure(figsize=(15,13)) 
    plt.savefig(filepath)


    data = {
    "status":"OK",
    "image":"/static/image/plot2.png",
    }

    return JsonResponse(data)

    # In[ ]:
def Plot3(request):

    tweetCount = pd.read_csv('totalcsv/tweetCount.csv')


    # In[165]:
    
    teams = pd.read_csv('totalcsv/teams.csv')


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
        df = pd.read_csv('totalcsv/'+row['Team']+'.csv')
        
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
    filepath = directory + '/app/static/image/plot3.png'
    if os.path.isfile(filepath):
        os.remove(filepath) 
    # plt.figure(figsize=(15,13)) 
    plt.savefig(filepath)
    plt.close()
   

    data = {
    "status":"OK",
    "image":"/static/image/plot3.png",
    }

    return JsonResponse(data)




