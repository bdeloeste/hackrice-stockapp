from django.shortcuts import render


# Create your views here.
def index(request):
    google_counter = 0
    microsoft_counter = 0
    facebook_counter = 0

    co_stocks = {'google': google_counter,
                 'microsoft': microsoft_counter,
                 'facebook': facebook_counter}

    return render(request, 'base.html', co_stocks)
