import requests
import json

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        print(f"Weather in {city}:")
        print(f"Main: {main_weather}")
        print(f"Description: {description}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
    else:
        print(f"Error fetching weather data for {city}. Status code: {response.status_code}")
 
# replace 'your_api_key' with your actual API key
get_weather('your_api_key', 'Paris')