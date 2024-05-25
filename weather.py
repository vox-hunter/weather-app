import requests
import geocoder
import time
from datetime import date
import os
from datetime import timedelta

def get_location():
    g = geocoder.ip('me')
    lat = g.latlng[0]
    lon = g.latlng[1]
    #print(round(lat, 2), round(lon, 2))
    return round(lat, 2), round(lon, 2)


def get_weather(lat, lon, unit="celsius"):
    call = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,wind_speed_10m,wind_direction_10m&hourly=temperature_2m,apparent_temperature,precipitation_probability,snow_depth,visibility,soil_temperature_0cm&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,daylight_duration,uv_index_max&past_days=1&temperature_unit={unit}&timezone=auto"
    raw = requests.get(call)
    data = raw.json()
    # temperatures
    generation = data["generationtime_ms"]
    current_time = data["current"]["time"]
    current_temperature = data["current"]["temperature_2m"]
    current_relative_humidity = data["current"]["relative_humidity_2m"]
    current_apparent_temperature = data["current"]["apparent_temperature"]
    current_rain = data["current"]["rain"]
    current_showers = data["current"]["showers"]
    current_wind_speed = data["current"]["wind_speed_10m"]
    current_wind_direction = data["current"]["wind_direction_10m"]
    hourly_times = data["hourly"]["time"]
    hourly_temperature = data["hourly"]["temperature_2m"]
    hourly_apparent_temperature = data["hourly"]["apparent_temperature"]
    hourly_precipitation_prob = data["hourly"]["precipitation_probability"]
    hourly_snow_depth = data["hourly"]["snow_depth"]
    hourly_visibility = data["hourly"]["visibility"]
    hourly_soil_temp = data["hourly"]["soil_temperature_0cm"]
    daily_times = data["daily"]["time"]
    daily_max_temp = data["daily"]["temperature_2m_max"]
    daily_min_temp = data["daily"]["temperature_2m_min"]
    daily_sunrise = data["daily"]["sunrise"]
    daily_sunset = data["daily"]["sunset"]
    daily_daylight_duration = data["daily"]["daylight_duration"]
    daily_uv_index_max = data["daily"]["uv_index_max"]
    yesterday_max_temp = 0
    yesterday_min_temp = 0
    # units
    daily_units_time = data["daily_units"]["time"]
    daily_units_temperature_max = data["daily_units"]["temperature_2m_max"]
    daily_units_temperature_min = data["daily_units"]["temperature_2m_min"]
    daily_units_sunrise = data["daily_units"]["sunrise"]
    daily_units_sunset = data["daily_units"]["sunset"]
    daily_units_daylight_duration = data["daily_units"]["daylight_duration"]
    daily_units_uv_index_max = data["daily_units"]["uv_index_max"]
    def convert(seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return '%d:%02d:%02d' % (hour, min, sec)
    t = time.localtime()
    current_time = time.strftime("%H", t)
    today = date.today()
    hour = f"{today}T{current_time}:00"
    for i in range(len(hourly_times)):
        if i < len(hourly_times):
            if hourly_times[i] == hour:
                hourly_temperature = hourly_temperature[i-1]
                hourly_apparent_temperature = hourly_apparent_temperature[i-1]
                hourly_precipitation_prob = hourly_precipitation_prob[i]
                hourly_snow_depth = hourly_snow_depth[i]
                hourly_visibility = hourly_visibility[i]
                hourly_soil_temp = hourly_soil_temp[i]
    for i in range(len(daily_times)):
        if str(today) in daily_times[i]:
            if i > 0 and str(today - timedelta(days=1)) in daily_times[i-1]:
                yesterday_max_temp = daily_max_temp[i-1]
                yesterday_min_temp = daily_min_temp[i-1] 
            daily_max_temp = daily_max_temp[i]
            daily_min_temp = daily_min_temp[i]
            daily_sunrise = daily_sunrise[i]
            daily_sunset = daily_sunset[i]
            daily_daylight_duration = daily_daylight_duration[i]
            daily_uv_index_max = daily_uv_index_max[i]
            print(daily_max_temp) 
                
    daily_sunrise = daily_sunrise.split("T")[1]
    daily_sunset = daily_sunset.split("T")[1]
    daily_daylight_duration = convert(daily_daylight_duration)
    return hourly_temperature, hourly_apparent_temperature, yesterday_max_temp, yesterday_min_temp, current_rain, current_showers,generation, current_temperature, current_relative_humidity, current_apparent_temperature, current_wind_speed, current_wind_direction, hourly_precipitation_prob, hourly_snow_depth, hourly_visibility, hourly_soil_temp, daily_max_temp, daily_min_temp, daily_sunrise, daily_sunset, daily_daylight_duration, daily_uv_index_max, daily_units_temperature_max, daily_units_temperature_min, daily_units_sunrise, daily_units_sunset, daily_units_daylight_duration, daily_units_uv_index_max


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def terminal():
    location = str(input("Please enter your city or press enter to use your current location: "))
    while True:
        clear_screen()  # Clear the screen before printing new weather data
        if location:
            raw = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=10&language=en&format=json")
            data = raw.json()
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
        else:
            lat, lon = get_location()

        hourly_temperature, hourly_apparent_temperature, yesterday_max_temp, yesterday_min_temp, rain, showers, generation,current_temperature, current_relative_humidity, current_apparent_temperature, current_wind_speed, current_wind_direction, hourly_precipitation_prob, hourly_snow_depth, hourly_visibility, hourly_soil_temp, daily_max_temp, daily_min_temp, daily_sunrise, daily_sunset, daily_daylight_duration, daily_uv_index_max, daily_units_temperature_max, daily_units_temperature_min, daily_units_sunrise, daily_units_sunset, daily_units_daylight_duration, daily_units_uv_index_max = get_weather(lat, lon)
        print(f"Weather generated in: {generation}")
        print(f"Current temperature: {current_temperature}°C")
        if round(current_temperature) > round(hourly_temperature):
            print(f"Current temperature is increased by {round(current_temperature - hourly_temperature)}°C than last hour")
        elif round(current_temperature) < round(hourly_temperature):
            print(f"Current temperature is decreased by {round(hourly_temperature - current_temperature)}°C than last hour")
        else:
            print(f"Current temperature hasn't changed since last hour")
        if round(current_apparent_temperature) > round(hourly_apparent_temperature):
            print(f"Current apparent temperature is increased by {round(current_apparent_temperature - hourly_apparent_temperature)}°C than last hour")
        elif round(current_apparent_temperature) < round(hourly_apparent_temperature):
            print(f"Current apparent temperature is decreased by {round(hourly_apparent_temperature - current_apparent_temperature)}°C than last hour")
        else:
            print(f"Current apparent temperature hasn't changed since last hour")
        if round(daily_max_temp) > round(yesterday_max_temp):
            print(f"Daily max temperature is increased by {round(daily_max_temp - yesterday_max_temp)}°C than yesterday")
        elif round(daily_max_temp) < round(yesterday_max_temp):
            print(f"Daily max temperature is decreased by {round(yesterday_max_temp - daily_max_temp)}°C than yesterday")
        else:
            print(f"Daily max temperature is same as yesterday")
        if round(daily_min_temp) > round(yesterday_min_temp):
            print(f"Daily min temperature is increased by {round(daily_min_temp - yesterday_min_temp)}°C than yesterday")
        elif round(daily_min_temp) < round(yesterday_min_temp):
            print(f"Daily min temperature is decreased by {round(yesterday_min_temp - daily_min_temp)}°C than yesterday")
        else:
            print(f"Daily min temperature is same as yesterday")
        print(f"Current relative humidity: {current_relative_humidity}%")
        print(f"Hourly precipitation probability: {hourly_precipitation_prob}%")
        print(f"Current rain: {rain}mm")
        print(f"Current showers: {showers}mm")
        print(f"Current wind speed: {current_wind_speed}m/s")
        print(f"Current wind direction: {current_wind_direction}°")
        if hourly_snow_depth == 0:
            print(f"Hourly snow depth: No snow")
        else:
            print(f"Hourly snow depth: {hourly_snow_depth}mm")
        print(f"Hourly visibility: {hourly_visibility}m")
        print(f"Hourly soil temperature: {hourly_soil_temp}°C")
        print(f"Daily sunrise: {daily_sunrise}")
        print(f"Daily sunset: {daily_sunset}")
        print(f"Daily daylight duration: {daily_daylight_duration}s")
        print(f"Daily UV index max: {daily_uv_index_max} {daily_units_uv_index_max}")

        time.sleep(30)


if __name__ == "__main__":
    terminal()