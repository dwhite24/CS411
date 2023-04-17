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
            w = processZip(form.cleaned_data["zip"])
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
    return json_result

def search_by_genre(token, genre):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=genre:{genre}&type=track&limit=10&offset=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_artist_genre(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    genres = json_result['artists']['items'][0]['genres']
    return genres

token = get_token()
#search_for_artist(token, "ACDC")
#search_by_genre(token, "Indie")

def requestWeather(zipcode):
    # REMEMBER TO ENV THIS!!!!!
    apikey = "dd397dd244344686bcc185144233103"

    requestlink = "https://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=yes".format(apikey, zipcode)
    r = requests.get(requestlink)
    content = r.json()
    dictf = json.loads(r.text)
    humidity = dictf["current"]["humidity"]
    weather = dictf["current"]["condition"]["text"]
    weatherid = dictf["current"]["condition"]["code"]
    temp_f = dictf["current"]["temp_f"]
    weather_info = [temp_f, weather, weatherid, humidity]

    return weather_info

def processZip(zipcode):
    weather = requestWeather(zipcode)
    weatherId = weather[2]
    if weatherId < 1006:
        return search_by_genre(token, "Indie")
    elif weatherId <1063:
        return search_by_genre(token, "Pop")
    elif weatherId < 1087:
        return search_by_genre(token, "Rock")
    elif weatherId == 1114 | weatherId == 1117 | (weatherId > 1209 & weatherId < 1238) | weatherId > 1248:
        return search_by_genre(token, "Jazz")
    else:
        return search_by_genre(token, "Disco")
    return weather