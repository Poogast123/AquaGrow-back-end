import joblib
import pandas as pd
import os

class ML:
    def __init__(self, path='res/predicting_model.joblib'):
        self.prediction = 0
        self.input_data = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, '..', 'res', 'predicting_model.joblib')

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Fichier introuvable : {model_path}")

        self.ml = joblib.load(model_path)
        self.feature_names = [
            'Soil Moisture', 'Temperature', ' Soil Humidity', 'Time',
            'Air temperature (C)', 'Wind speed (Km/h)', 'Air humidity (%)'
        ]

    def set_input_data(self, Soil_Moisture, Temperature, Soil_Humidity, Time, Air_temperature, Wind_speed,
                       Air_humidity):
        self.input_data = [Soil_Moisture, Temperature, Soil_Humidity, Time, Air_temperature, Wind_speed, Air_humidity]

    def set_prediction(self):
        df_input_data = pd.DataFrame([self.input_data], columns=self.feature_names)
        self.prediction = self.ml.predict(df_input_data)
        return self.prediction