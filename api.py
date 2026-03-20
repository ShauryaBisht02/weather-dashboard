import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
try:
    API_KEY = st.secrets["API_KEY"]
except:
    API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_current_weather(city):
    url = f"{BASE_URL}/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"]
        }
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.ConnectionError:
        return "connection_error"

def get_forecast(city):
    url = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric", "cnt": 40}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        daily = {}
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily:
                daily[date] = {"temps": [], "descriptions": [], "icons": []}
            daily[date]["temps"].append(item["main"]["temp"])
            daily[date]["descriptions"].append(item["weather"][0]["description"])
            daily[date]["icons"].append(item["weather"][0]["icon"])
        forecast = []
        for date, values in list(daily.items())[:5]:
            forecast.append({
                "date": date,
                "min_temp": round(min(values["temps"]), 1),
                "max_temp": round(max(values["temps"]), 1),
                "description": values["descriptions"][0].capitalize(),
                "icon": values["icons"][0]
            })
        return forecast
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.ConnectionError:
        return "connection_error"