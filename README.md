# Weather App

This is a simple weather application built using Streamlit that fetches and displays weather data based on the user's location or a manually entered city.

You can view the live app [here](https://weather-web-app.streamlit.app).
**This app is no longer updated**

## Features

- Fetches weather data based on current location or entered city
- Displays current temperature, apparent temperature, maximum a temperatures
- Provides warnings for excessive heat
- Shows additional weather details such as precipitation, wind speed, and direction, visibility, soil temperature, sunrise and sunset times, and UV index
- Interactive UI with temperature unit selection (°C or °F)
- Rain and snow animations for visual appeal

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
2. Install the required packages
   ```sh
   pip install -r requirements.txt

## Usage
  To run the application, execute the following command:
  streamlit run app.py

## How to use
1. Open the application in your browser.
2. Enter your city name in the text input box or press enter to use your current location.
3. Select your preferred temperature unit (°C or °F).
4. View the fetched weather data and additional information displayed on the screen.
5. If rain or snow is detected, enjoy the animations!

## Acknowledgements
Open-Meteo for weather data

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/vox-hunter/weather-app/blob/main/LICENSE) file for details.
