from weather import get_weather
import streamlit as st
import time
import requests
from streamlit_extras.let_it_rain import rain
from streamlit_extras.bottom_container import bottom
from streamlit_js_eval import get_geolocation
from streamlit_lottie import st_lottie

key = "9ScW6YjbnCvRR9wClJVkbgoJsonPcmpy"

def get_info(lat, lon, unit="celsius"):
    data = get_weather(lat, lon, unit=unit)
    return data

def get_location():
    # Get the location
    try:
        loc = get_geolocation()
        lat = loc["coords"]["latitude"]
        lon = loc["coords"]["longitude"]
    except Exception as e:
        raise ValueError("An error occurred while getting the location.")
        return
    return round(lat, 2), round(lon, 2)

def additional_info(lat, lon):
    raw = requests.get(f"https://api.pirateweather.net/forecast/{key}/{lat},{lon}")
    data = raw.json()
    return data

def heat_index(temperature, humidity, unit="celsius"):
    # for warnings
    if unit == "celsius":
        temperature = temperature * 9/5 + 32
    else:
        temperature = temperature
    # Constants
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -6.83783e-3
    c6 = -5.481717e-2
    c7 = 1.22874e-3
    c8 = 8.5282e-4
    c9 = -1.99e-6

    # Heat index formula
    heat_index = (c1 + (c2 * temperature) + (c3 * humidity) + (c4 * temperature * humidity) + 
                  (c5 * temperature ** 2) + (c6 * humidity ** 2) + 
                  (c7 * temperature ** 2 * humidity) + (c8 * temperature * humidity ** 2) + 
                  (c9 * temperature ** 2 * humidity ** 2))
    
    return heat_index

def main():
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.title("Weather App")
    location = st.text_input("Please enter your city or enter to use your current location: ").strip().upper()
    if location:
        raw = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=10&language=en&format=json")
        data = raw.json()
        try:
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
        except Exception as e:
            st.error(f"Please enter an valid location")
            return
    else:
        try:
            location = get_location()
            if location is None:
                st.error("Please allow your location or enter a location manually.")
                return
            else:
                lat, lon = location
        except ValueError as e:
            st.error(f"Please allow your location or enter a location manually.")
            return
    option = st.selectbox(
   "Change temperature unit:",
   ("°C", "°F"),
   index=None,
   placeholder="Select a unit...",
)   
    with bottom():
        st.write("Made by Vox Hunter with ❤️")
    if option == None:
        option = "°C"
    if option == "°F":
        try:
            data = get_info(lat, lon, unit="fahrenheit")
            if data is None:
                raise ValueError("No data returned from get_info")
        except requests.exceptions.ConnectionError:
            st.error("No internet connection! Please check your connection and try again.")
            return
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return
    else:
        try:
            data = get_info(lat, lon, unit="celsius")
            if data is None:
                raise ValueError("No data returned from get_info")
        except requests.exceptions.ConnectionError:
            st.error("No internet connection! Please check your connection and try again.")
            return
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return
    
    # Unpack the data
    hourly_temperature, hourly_apparent_temperature, yesterday_max_temp, yesterday_min_temp, rain_amount, showers, generationtime_ms, current_temperature, current_relative_humidity, current_apparent_temperature, current_wind_speed, current_wind_direction, hourly_precipitation_prob, hourly_snow_depth, hourly_visibility, hourly_soil_temp, daily_max_temp, daily_min_temp, daily_sunrise, daily_sunset, daily_daylight_duration, daily_uv_index_max, daily_units_temperature_max, daily_units_temperature_min, daily_units_sunrise, daily_units_sunset, daily_units_daylight_duration, daily_units_uv_index_max = data
    with st.status("Downloading data..."):
        st.write("Fetching Weather Data...")
        time.sleep(1)
        if data:
            st.write("Data Fetched!")
            st.toast('Data Fetched!')
        time.sleep(0.5)
        st.write("Extracting Data...")
        time.sleep(0.5)
        st.write(f"Process has been completed in {round(generationtime_ms, 2)}ms")
        st.toast("Succesfully Completed!")
        st.success("Data Extracted!")
    # Additional info
    additional_data = additional_info(lat, lon)
    if additional_data["hourly"]["icon"] == "cloudy":
        pass
    temp, app_temp, max_temp, min_temp = st.columns(4)
    # Display the weather data
    # Current temperature
    if option == "°C":
        heat_index_value = heat_index(current_temperature, current_relative_humidity)
        try:
            if additional_data["alerts"]:
                st.warning(f"Alert: {additional_data['alerts']['title']}", icon="⚠️")
        except KeyError:
            pass
        if heat_index_value > 80:
            st.warning("Excessive Heat Warning! Take precautions to avoid heat-related illnesses.", icon="⚠️")
        if round(current_temperature) > round(hourly_temperature):
                temp.metric("Current Temp", f"{current_temperature}°C", f"{round(current_temperature - hourly_temperature)}°C", delta_color="inverse")
        elif round(current_temperature) < round(hourly_temperature):
                temp.metric("Current Temp", f"{current_temperature}°C", f"-{round(hourly_temperature - current_temperature)}°C", delta_color="inverse")
        else:
                temp.metric("Current Temp", f"{current_temperature}°C", "No Change", delta_color="off")
        # Apparent temperature
        if round(current_apparent_temperature) > round(hourly_apparent_temperature):
            app_temp.metric("Apparent Temp", f"{current_apparent_temperature}°C", f"{round(current_apparent_temperature - hourly_apparent_temperature)}°C", delta_color="inverse")
        elif round(current_apparent_temperature) < round(hourly_apparent_temperature):
            app_temp.metric("Apparent Temp", f"{current_apparent_temperature}°C", f"-{round(hourly_apparent_temperature - current_apparent_temperature)}°C", delta_color="inverse")
        else:
            app_temp.metric("Apparent Temp", f"{current_apparent_temperature}°C", "No Change", delta_color="off")
        # Max and Min temperature
        if round(daily_max_temp) > round(yesterday_max_temp):
            max_temp.metric("Max Temperature today:", f"{daily_max_temp}°C", f"{round(daily_max_temp - yesterday_max_temp)}°C", delta_color="inverse")
        elif round(daily_max_temp) < round(yesterday_max_temp):
            max_temp.metric("Max Temperature today:", f"{daily_max_temp}°C", f"-{round(yesterday_max_temp - daily_max_temp)}°C", delta_color="inverse")
        else:
            max_temp.metric("Max Temperature today:", f"{daily_max_temp}°C", "No Change", delta_color="off")
        if round(daily_min_temp) > round(yesterday_min_temp):
            min_temp.metric("Min Temperature today:", f"{daily_min_temp}°C", f"{round(daily_min_temp - yesterday_min_temp)}°C", delta_color="inverse")
        elif round(daily_min_temp) < round(yesterday_min_temp):
            min_temp.metric("Min Temperature today:", f"{daily_min_temp}°C", f"-{round(yesterday_min_temp - daily_min_temp)}°C", delta_color="inverse")
        else:
            min_temp.metric("Min Temperature today:", f"{daily_min_temp}°C", "No Change", delta_color="off")
    if option == "°F":
        heat_index_value = heat_index(current_temperature, current_relative_humidity, unit="fahrenheit")
        if round(current_temperature) > round(hourly_temperature):  
                temp.metric("Current Temp", f"{current_temperature}°F", f"{round(current_temperature - hourly_temperature)}°F", delta_color="inverse")
        elif round(current_temperature) < round(hourly_temperature):
                temp.metric("Current Temp", f"{current_temperature}°F", f"-{round(hourly_temperature - current_temperature)}°F", delta_color="inverse")
        else:
                temp.metric("Current Temp", f"{current_temperature}°F", "No Change", delta_color="off")
        # Apparent temperature
        if round(current_apparent_temperature) > round(hourly_apparent_temperature):
            app_temp.metric("Apparent Temp", f"{current_apparent_temperature}°F", f"{round(current_apparent_temperature - hourly_apparent_temperature)}°F", delta_color="inverse")
        elif round(current_apparent_temperature) < round(hourly_apparent_temperature):
            app_temp.metric("Apparent Temp", f"{current_apparent_temperature}°F", f"-{round(hourly_apparent_temperature - current_apparent_temperature)}°F", delta_color="inverse")
        else:
            app_temp.metric("Apparent Temp", f"{current_apparent_temperature}°F", "No Change", delta_color="off")
        # Max and Min temperature
        if round(daily_max_temp) > round(yesterday_max_temp):
            max_temp.metric("Max Temperature today:", f"{daily_max_temp}°F", f"{round(daily_max_temp - yesterday_max_temp)}°F", delta_color="inverse")
        elif round(daily_max_temp) < round(yesterday_max_temp):
            max_temp.metric("Max Temperature today:", f"{daily_max_temp}°F", f"-{round(yesterday_max_temp - daily_max_temp)}°F", delta_color="inverse")
        else:
            max_temp.metric("Max Temperature today:", f"{daily_max_temp}°F", "No Change", delta_color="off")
        if round(daily_min_temp) > round(yesterday_min_temp):
            min_temp.metric("Min Temperature today:", f"{daily_min_temp}°F", f"{round(daily_min_temp - yesterday_min_temp)}°F", delta_color="inverse")
        elif round(daily_min_temp) < round(yesterday_min_temp):
            min_temp.metric("Min Temperature today:", f"{daily_min_temp}°C", "No Change", delta_color="off")
    st.write(f"Chance of Rain: {hourly_precipitation_prob}%")
    st.write(f"Relative Humidity: {current_relative_humidity}%")

    if rain_amount > 0:
        rain(emoji="💧",font_size=20,falling_speed=5,animation_length="infinite")
    if showers > 0:
        st.write(f"Showers: {showers}mm")
    st.write(f"Wind Speed: {current_wind_speed}m/s")
    st.write(f"Wind Direction: {current_wind_direction}°")
    if hourly_snow_depth > 0:
        st.write(f"Snow Depth: {hourly_snow_depth}mm")
        rain(emoji="❄️",font_size=20,falling_speed=3,animation_length="infinite")
    st.write(f"Visibility: {hourly_visibility}m")
    st.write(f"Soil Temperature: {hourly_soil_temp}°C")
    st.write(f"Sunrise: {daily_sunrise}")
    st.write(f"Sunset: {daily_sunset}")
    st.write(f"Daylight Duration: {daily_daylight_duration}s")
    st.write(f"UV Index Max: {daily_uv_index_max} {daily_units_uv_index_max}")

if __name__ == "__main__":
    main()
