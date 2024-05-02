import requests
import json

def get_weather(api_key, city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        pressure = main["pressure"]
        weather_report = data["weather"]
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print(f"Weather Report: {weather_report[0]['description']}")
    else:
        print("Error: Invalid city: {city} or wrong API key")

# replace 'your_api_key' with your actual API key
api_key = "your_api_key"
city = "Paris"
get_weather(api_key, city)