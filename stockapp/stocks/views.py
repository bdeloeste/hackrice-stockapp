import tweepy

from django.shortcuts import render


# Create your views here.
def index(request):
    google_counter = 0
    twitter_counter = 0
    facebook_counter = 0

    co_stocks = {'google': google_counter,
                 'twitter': twitter_counter,
                 'facebook': facebook_counter}

    return render(request, 'base.html', {})
