from weather import get_weather
import streamlit as st
import time
import requests
from streamlit_extras.let_it_rain import rain
from streamlit_extras.bottom_container import bottom
from streamlit_js_eval import get_geolocation
from streamlit_lottie import st_lottie

# Implementing the weather app using classes
class Weather:
    def get_weather(self, lat=0, lon=0):
        # Get the user's location
        location = get_geolocation()
        if lat!=0 and lon!=0:
            lat = location["latitude"]
            lon = location["longitude"]
        # Get the weather
        weather = get_weather(lat, lon)
        return weather
    