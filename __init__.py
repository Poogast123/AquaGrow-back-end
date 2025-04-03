from flask import Flask, jsonify, request
from flask_cors import CORS
from app.conductor import MainApplication
import threading
import time
from app.weatherapi import WeatherApi
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

main_app = MainApplication()
robot_decision = {"status": None, "override": None}
d = WeatherApi()
collected_data = []

def daily_irrigation_check():
    global collected_data
    while True:
        time.sleep(86400)
        soil_moisture = main_app.get_soil_moisture_from_sensor()
        soil_humidity = main_app.get_soil_humidity_from_sensor()

        main_app.set_Soil_Moisture(soil_moisture)
        main_app.set_Soil_Humidity(soil_humidity)
        prediction = main_app.make_prediction()

        collected_data = d.getToDayStates()
        collected_data.append(soil_moisture)
        collected_data.append(soil_humidity)

        robot_decision["status"] = "Irrigate" if prediction else "Do Not Irrigate"
        robot_decision["override"] = None

threading.Thread(target=daily_irrigation_check, daemon=True).start()

@app.route('/override', methods=['POST'])
def override_decision():
    data = request.json
    decision = data.get("decision")
    if decision in ["Irrigate", "Do Not Irrigate"]:
        with open("override.txt", "w") as file:
            file.write(decision)
        # Log decision history
        with open("history.txt", "a") as history_file:
            history_file.write(f"{decision} - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        return jsonify({"message": f"Decision overridden to: {decision}"})
    else:
        return jsonify({"error": "Invalid decision"}), 400


@app.route('/weather', methods=['POST'])
def get_weather_data():
    """API to get both weather and soil data"""
    data = {
        "weather_data": d.getToDayStates(),
        "soil_moisture": main_app.get_soil_moisture_from_sensor(),
        "soil_humidity": main_app.get_soil_humidity_from_sensor(),
        "robot_decision": robot_decision["status"]
    }
    return jsonify(data)

@app.route('/predict', methods=['POST'])
def predict():
    """API to make a prediction based on soil data"""
    data = request.json
    soil_moisture = data.get("Soil_Moisture")
    soil_humidity = data.get("Soil_Humidity")

    main_app.set_Soil_Moisture(soil_moisture)
    main_app.set_Soil_Humidity(soil_humidity)
    prediction = main_app.make_prediction()

    return jsonify({"prediction": "Irrigate" if prediction else "Do Not Irrigate"})

@app.route('/history', methods=['GET'])
def get_history():
    """Returns past irrigation decisions"""
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as file:
            history_data = file.readlines()
        return jsonify({"history": [entry.strip() for entry in history_data]})
    else:
        return jsonify({"history": []})

if __name__ == "__main__":
    app.run(debug=True, port=5002)
