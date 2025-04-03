import openmeteo_requests
import requests_cache
from retry_requests import retry

class WeatherApi:
    def __init__(self, Temperature=0, Air_Temperature=0, Wind_Speed=0, Air_Humidity=0, weather_code=0,Time = 0):
        self.Temperature = Temperature
        self.Air_Temperature = Air_Temperature
        self.Wind_Speed = Wind_Speed
        self.Air_Humidity = Air_Humidity
        self.weather_code = weather_code
        self.Time = Time

    def API(self):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 52.52,
            "longitude": 13.41,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code",
                        "wind_speed_10m"],
            "timeformat": "unixtime"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]


        # Current values. The order of variables needs to be the same as requested.
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        self.Temperature = current.Variables(0).Value()
        current_relative_humidity_2m = current.Variables(1).Value()
        self.Air_Humidity = current.Variables(1).Value()
        current_apparent_temperature = current.Variables(2).Value()
        self.Air_Temperature = current.Variables(2).Value()
        current_weather_code = current.Variables(3).Value()
        self.weather_code = current.Variables(3).Value()
        current_wind_speed_10m = current.Variables(4).Value()
        self.Wind_Speed = current.Variables(4).Value()
        self.Time = current.Time()

    def getToDayStates(self):
        self.API()
        return [self.Temperature, self.Air_Temperature, self.Air_Humidity, self.Time, self.Wind_Speed]



