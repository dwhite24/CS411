import os
from django.shortcuts import render, redirect
from django.template import loader
from django import forms
from django.db import models
from .models import UserSave
import requests
import json
import base64
import random
from requests import post, get
from django.http import HttpResponse

def index(request):
    return render(request, 'protype.html')


def profile(request):
    try:
        usersave = UserSave.objects.get(user=request.user)
        urls = list(usersave.songs.split(" "))
        context = {'usersave': urls}
    except UserSave.DoesNotExist:
        return render(request, 'profile.html')
    return render(request, 'profile.html', context)


class protypeForm(forms.Form):
    zip = forms.CharField(max_length=10)

def protype(request):
    if request.method == 'POST':
        form = protypeForm(request.POST)
        if form.is_valid():


            # Takes in a zip code and returns the weather situation in temp_f, condition, and humidity
            w = requestWeather(form.cleaned_data["zip"])
            track = processZip(form.cleaned_data["zip"])
            print(form.cleaned_data["zip"])
            track_uri = track
            url = f'https://open.spotify.com/embed/track/{track_uri.split(":")[2]}'
            print(url)
            #context = {'weather': w, "form": form}
            context = {'weather': "", "country": w[8], "location": w[6], "region": w[7],"temp_c": w[5], "temperature": w[0],"condition": w[1], "humidity": w[3], "icon": w[4],"form": form, "embed_link": url}

            try:
                usersave = UserSave.objects.get(user=request.user)
                string = " " + url
                usersave.songs += string
                usersave.save()
            except UserSave.DoesNotExist:
                usersave = UserSave(user=request.user, songs=url)
                usersave.save()

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
    query = f"?q=genre:{genre}&type=track&offset=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    song_name = json_result["tracks"]["items"][1]["name"]
    song_preview = json_result["tracks"]["items"][1]["preview_url"]
    return json_result#["tracks"]["items"][1]["preview_url"]

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
    weathericon = dictf["current"]["condition"]["icon"]
    temp_f = dictf["current"]["temp_f"]
    temp_c = dictf["current"]["temp_c"]
    location_name = dictf["location"]["name"]
    location_region = dictf["location"]["region"]
    location_country = dictf["location"]["country"]

    weather_info = [temp_f, weather, weatherid, humidity, weathericon, temp_c, location_name, location_region, location_country]

    return weather_info

def processZip(zipcode):
    weather = requestWeather(zipcode)
    weatherId = weather[2]
    if weatherId < 1006:
        result = search_by_genre(token, "Indie")

    elif weatherId <1063:
        result = search_by_genre(token, "Pop")

    elif weatherId < 1087:
        result = search_by_genre(token, "Rock")
 
    elif weatherId == 1114 | weatherId == 1117 | (weatherId > 1209 & weatherId < 1238) | weatherId > 1248:
        result = search_by_genre(token, "Jazz")

    else:
        result = search_by_genre(token, "Disco")
    
    return returnRandomSongURI(result)

def returnRandomSongURI(list):
    newList = list['tracks']['items']
    num = random.randint(0,len(newList))
    print("# of results: ", len(newList))
    print(num)
    return newList[num]['uri']


