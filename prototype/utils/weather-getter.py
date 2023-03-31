import requests
import json


# Takes in a zip code and returns the weather situation in temp_f, condition, and humidity
def requestWeather(zipcode):

    # REMEMBER TO ENV THIS!!!!!
    apikey = "dd397dd244344686bcc185144233103"

    zipcode = str(zipcode)
    requestlink = "https://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=yes".format(apikey, zipcode)
    r = requests.get(requestlink)
    content = r.json()
    dictf = json.loads(r.text)


    humidity = dictf["current"]["humidity"]
    weather = dictf["current"]["condition"]["text"]
    temp_f = dictf["current"]["temp_f"]
    weather_info = [temp_f, weather, humidity]
    

    return weather_info


print(requestWeather("02134"))
