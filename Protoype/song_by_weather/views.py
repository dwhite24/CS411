from django.shortcuts import render, redirect
from django.template import loader
from django import forms
import requests
import json
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class protypeForm(forms.Form):
    zip = forms.CharField(max_length=10)

def protype(request):
    if request.method == 'POST':
        form = protypeForm(request.POST)
        if form.is_valid():


            # Takes in a zip code and returns the weather situation in temp_f, condition, and humidity
            w = requestWeather(form.cleaned_data["zip"])
            print(form.cleaned_data["zip"])
            context = {'weather': w, "form": form}
        else:
            context = {'weather': 'invalid form', "form": form}
    else:
        form = protypeForm()
        context = {'weather': 'none', "form": form}


    return render(request, 'protype.html', context=context)


def requestWeather(zipcode):
    # REMEMBER TO ENV THIS!!!!!
    apikey = "dd397dd244344686bcc185144233103"

    requestlink = "https://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=yes".format(apikey, zipcode)
    r = requests.get(requestlink)
    content = r.json()
    dictf = json.loads(r.text)
    humidity = dictf["current"]["humidity"]
    weather = dictf["current"]["condition"]["text"]
    temp_f = dictf["current"]["temp_f"]
    weather_info = [temp_f, weather, humidity]

    return weather_info