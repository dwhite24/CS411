import os
from django.shortcuts import render, redirect
from django.template import loader
from django import forms
import requests
import json
import base64
from requests import post, get
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

def requestMusic(weather_info):
    #This function should return the music based on the weather
    return NotImplemented

#NEED TO ENV THIS
client_id = "c6dd25d2b96d44e09597035c532b1101"#os.getenv("CLIENT_ID")
client_secret = "562d9f95ab8a4c218416405f42805b6d"#os.getenv("CLIENT_SECRET")
def get_token():
    #gets spotify api token
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    print(json_result)

token = get_token()
search_for_artist(token, "ACDC")

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