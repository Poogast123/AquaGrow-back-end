# AquaFriend/AquaFriend/README.md

# AQUAFRIEND

This project is a Flask-based API that integrates weather data and machine learning predictions for soil moisture management. It utilizes the Open-Meteo API to fetch current weather conditions and a pre-trained machine learning model to make predictions based on the weather data and soil conditions.

## Project Structure

```
AquaFriend
├── app
│   ├── __init__.py          # Initializes the Flask application and sets up routes
│   ├── conductor.py         # Manages interaction between the weather API and ML model
│   ├── ml.py                # Defines the ML class for predictions
│   ├── weatherapi.py        # Interacts with the Open-Meteo API for weather data
│   └── routes
│       └── api.py           # Defines API routes for the application
├── requirements.txt         # Lists project dependencies
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd AquaFriend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   flask run
   ```

## Usage

Once the application is running, you can access the API endpoints defined in `app/routes/api.py`. The API allows you to interact with the weather data and make predictions based on soil moisture and humidity.

## Example

To get a prediction, you can send a POST request to the appropriate endpoint with the required parameters.

## License

This project is licensed under the MIT License. See the LICENSE file for details.