from app.weatherapi import WeatherApi
from app.ml import ML


class MainApplication:
    def __init__(self):
        self.weather = WeatherApi()
        self.soil_moisture = 63
        self.soil_humidity = 45
        self.ml = ML()

    def set_Soil_Moisture(self, value):
        self.soil_moisture = value

    def get_soil_moisture_from_sensor(self):
        """Returns the current soil moisture value"""
        return self.soil_moisture

    def set_Soil_Humidity(self, value):
        self.soil_humidity = value

    def get_soil_humidity_from_sensor(self):
        """Returns the current soil humidity value"""
        return self.soil_humidity

    def make_prediction(self):
        self.weather.API()
        self.ml.set_input_data(self.soil_moisture, self.weather.Temperature, self.soil_humidity,
                               self.weather.Time, self.weather.Air_Temperature, self.weather.Wind_Speed, self.weather.Air_Humidity)
        prediction = self.ml.set_prediction()[0]
        return prediction
