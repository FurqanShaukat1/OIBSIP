from assistant.weather import WeatherService


weather = WeatherService()

result = weather.get_weather("Karachi")

print(result)