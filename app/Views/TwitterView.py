
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def tweetshow(request):
    return render(request,"twitter/tweets.html")




