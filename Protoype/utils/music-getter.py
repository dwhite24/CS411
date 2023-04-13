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