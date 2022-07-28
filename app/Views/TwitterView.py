
from django.shortcuts import render



def tweetshow(request):
    return render(request,"twitter/tweets.html")




