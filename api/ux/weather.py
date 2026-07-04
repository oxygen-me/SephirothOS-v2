# --- imports
import requests

# --- create Weather class
class Weather:

    # --- define weather codes
    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    def __init__(self):
        self.city = None
        self.lat = None
        self.lon = None

    def get_location(self):
        location = requests.get("https://ipapi.co/json").json()

        self.city = location["city"]
        self.lat = location["latitude"]
        self.lon = location["longitude"]

    def get_weather(self):
        if self.lat is None:
            self.get_location()

        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": "temperature_2m,weather_code",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
        }

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params=params,
        ).json()

        return {
            "city": self.city,
            "temperature": weather["current"]["temperature_2m"],
            "condition": self.WEATHER_CODES.get(
                weather["current"]["weather_code"], "Unknown"
            ),
        }