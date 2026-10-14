from weather_service import WeatherService


service = WeatherService()

forecast = service.get_forecast("Karachi")

print("\nFORECAST TEST")
print("-" * 40)

for item in forecast[:6]:
    print(
        item["dt_txt"],
        "|",
        item["main"]["temp"],
        "°C",
        "|",
        item["weather"][0]["description"]
    )