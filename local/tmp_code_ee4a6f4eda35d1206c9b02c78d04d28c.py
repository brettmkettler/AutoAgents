import requests
import json

def get_weather(api_key, city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        weather_report = data['weather']
        print("Temperature : " +
                        str(temperature) +
              "\nHumidity : " +
                        str(humidity) +
              "\nWeather Report : " +
                        str(weather_report[0]['description']))
    else:
        print("Invalid city: " + city)
    
# replace 'your_api_key' with your actual OpenWeatherMap api key
get_weather('your_api_key', 'Paris')