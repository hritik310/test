from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.views.decorators.csrf import csrf_exempt






# In[117]:
@csrf_exempt
def nfl(request):
    df = pd.read_csv('totalcsv/eloDF.csv') 
    
    z=df.to_dict()  
    team=z["Team"]
    rating=z["Elo Rating"]
    team_list=list(team.values())
    rating_list=list(rating.values())

    return render(request,"signup/nfl.html",{"team_list":team_list,"rating_list":rating_list})