import json
import os

from django.shortcuts import render


# Create your views here.
def index(request):
    google_counter = 154.54
    microsoft_counter = 12
    facebook_counter = 0

    co_stocks = {'google': google_counter,
                 'microsoft': microsoft_counter,
                 'facebook': facebook_counter}

    with open("stock_data.json", "w") as outfile:
        json.dump(co_stocks, outfile)

    return render(request, 'base.html', co_stocks)
