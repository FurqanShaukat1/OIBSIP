import requests
from config import OPENWEATHER_API_KEY


class WeatherService:

    CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    def get_weather(self, city):

        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(
                self.CURRENT_URL,
                params=params,
                timeout=10
            )

            if response.status_code == 404:
                raise ValueError("City not found.")

            if response.status_code == 401:
                raise ValueError("Invalid or expired API key.")

            response.raise_for_status()

            data = response.json()

            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "visibility": round(
                    data.get("visibility", 0) / 1000,
                    1
                ),
                "icon": data["weather"][0]["icon"]
            }

        except requests.exceptions.Timeout:
            raise ConnectionError(
                "The weather service timed out."
            )

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Unable to connect to the weather service."
            )

    def get_forecast(self, city):

        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        try:

            response = requests.get(
                self.FORECAST_URL,
                params=params,
                timeout=10
            )

            print("FORECAST STATUS:", response.status_code)

            if response.status_code == 404:
                raise ValueError("City not found.")

            if response.status_code == 401:
                raise ValueError(
                    "Invalid or expired API key."
                )

            response.raise_for_status()

            data = response.json()

            print(
                "FORECAST ITEMS:",
                len(data.get("list", []))
            )

            return data.get("list", [])

        except requests.exceptions.Timeout:
            raise ConnectionError(
                "Forecast request timed out."
            )

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Unable to connect to forecast service."
            )