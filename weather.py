from requests import get
from bs4 import BeautifulSoup as BS 
from json import loads
import datetime



def weather(city_name):

    resp = get('http://api.openweathermap.org/data/2.5/weather?q='+ city_name +'&units=metric&appid=openweather_api_key')
    soup = BS(resp.text,'html.parser')
    all_data = soup.prettify()
    #all_info = resp.json()
    all_info = loads(all_data)

    icon_code = str(all_info["weather"][0]["icon"])

    time = {
    'sunrise_time_unix' : all_info["sys"]["sunrise"],
    'sunset_time_unix' : all_info["sys"]["sunset"]
    }

    main_info = {
    'long_value' : str(all_info["coord"]["lon"]),
    'lat_value' : str(all_info["coord"]["lat"]),
    'weather_main' : all_info["weather"][0]["main"],
    'weather_disc' : all_info["weather"][0]["description"],
    'temp_now' : str(all_info["main"]["temp"]),
    'temp_feels' : str(all_info["main"]["feels_like"]),
    'visibility_info' : str(all_info["visibility"]),
    'wind_speed' : str(all_info["wind"]["speed"]),
    'cloud_info' : str(all_info["clouds"]["all"]),
    'pressure_value' : str(all_info["main"]["pressure"]),
    'humidity_percentage' : str(all_info["main"]["humidity"]),
    'country_code' : all_info["sys"]["country"],
    'place_name' : all_info["name"],
    'sunrise_time' : (datetime.datetime.fromtimestamp(int(time['sunrise_time_unix'])) + datetime.timedelta(hours=5, minutes=30)).strftime('%H:%M:%S'),
    'sunset_time' : (datetime.datetime.fromtimestamp(int(time['sunset_time_unix'])) + datetime.timedelta(hours=5, minutes=30)).strftime('%H:%M:%S'),
    'icon_url' : "http://openweathermap.org/img/wn/"+icon_code+"@2x.png"
    }


    return main_info

