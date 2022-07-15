from sportsipy.nfl.boxscore import Boxscores
import pandas as pd
from app.models import Modelvar
import numpy as np
import xgboost as xgb
from django.http import JsonResponse
from django.shortcuts import render







def newprediction(request):
              
    return render(request,"signup/prediction.html")
