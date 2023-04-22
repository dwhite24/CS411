from django.shortcuts import render, redirect
from django.template import loader
from django import forms
import requests
import json
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
