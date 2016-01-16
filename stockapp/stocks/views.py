import tweepy

from django.shortcuts import render


# Create your views here.
def index(request):
    google_counter = 0
    twitter_counter = 0
    facebook_counter = 0

    co_stocks = {}

    return render(request, 'base.html', {})
