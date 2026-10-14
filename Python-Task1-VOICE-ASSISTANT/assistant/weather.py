import os

import requests
from dotenv import load_dotenv


load_dotenv()


class WeatherService:

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, city):
        if not self.api_key:
            return "The weather API key is not configured."

        if not city:
            return "Please tell me which city you want the weather for."

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=10
            )

            if response.status_code == 404:
                return f"I couldn't find the city {city}."

            response.raise_for_status()

            data = response.json()

            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            return (
                f"The weather in {city} is {description}. "
                f"The temperature is {temperature:.1f} degrees Celsius, "
                f"feels like {feels_like:.1f} degrees, "
                f"with humidity at {humidity} percent."
            )

        except requests.exceptions.Timeout:
            return "The weather service took too long to respond."

        except requests.exceptions.RequestException:
            return "I couldn't connect to the weather service."

        except (KeyError, TypeError, ValueError):
            return "I received an unexpected response from the weather service."