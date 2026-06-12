from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from functools import lru_cache

app = Flask(__name__)

# OpenWeatherMap API key (free tier)
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY", "YOUR_API_KEY_HERE")
OPEN_WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Cache weather data for 10 minutes
@lru_cache(maxsize=100)
def get_weather_data(city, api_key):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        url = f"{OPEN_WEATHER_BASE_URL}/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Use Celsius
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}

def get_forecast_data(city, api_key):
    """Fetch 5-day weather forecast from OpenWeatherMap API"""
    try:
        url = f"{OPEN_WEATHER_BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch forecast data: {str(e)}"}

def parse_weather_response(data):
    """Parse OpenWeatherMap response into readable format"""
    if "error" in data:
        return data
    
    try:
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "wind_speed": data["wind"]["speed"],
            "clouds": data["clouds"]["all"],
            "visibility": data.get("visibility", "N/A"),
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S"),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")
        }
    except KeyError as e:
        return {"error": f"Invalid API response: {str(e)}"}

@app.route("/", methods=["GET"])
def home():
    """Serve the weather dashboard HTML"""
    return render_template("index.html")

@app.route("/api/weather", methods=["GET"])
def get_weather():
    """API endpoint to get current weather for a city"""
    city = request.args.get("city", "London")
    
    if not OPEN_WEATHER_API_KEY or OPEN_WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return jsonify({"error": "OpenWeatherMap API key not configured"}), 400
    
    weather_data = get_weather_data(city, OPEN_WEATHER_API_KEY)
    parsed_data = parse_weather_response(weather_data)
    
    if "error" in parsed_data:
        return jsonify(parsed_data), 400
    
    return jsonify(parsed_data)

@app.route("/api/forecast", methods=["GET"])
def get_forecast():
    """API endpoint to get 5-day weather forecast for a city"""
    city = request.args.get("city", "London")
    
    if not OPEN_WEATHER_API_KEY or OPEN_WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return jsonify({"error": "OpenWeatherMap API key not configured"}), 400
    
    forecast_data = get_forecast_data(city, OPEN_WEATHER_API_KEY)
    
    if "error" in forecast_data:
        return jsonify(forecast_data), 400
    
    # Parse forecast data (every 3 hours for 5 days)
    forecasts = []
    for item in forecast_data.get("list", []):
        forecasts.append({
            "datetime": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M"),
            "temperature": item["main"]["temp"],
            "weather": item["weather"][0]["main"],
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
            "humidity": item["main"]["humidity"],
            "wind_speed": item["wind"]["speed"]
        })
    
    return jsonify({
        "city": forecast_data["city"]["name"],
        "country": forecast_data["city"]["country"],
        "forecasts": forecasts
    })

@app.route("/api/weather/multiple", methods=["POST"])
def get_multiple_cities():
    """API endpoint to get weather for multiple cities at once"""
    cities = request.get_json().get("cities", [])
    
    if not OPEN_WEATHER_API_KEY or OPEN_WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return jsonify({"error": "OpenWeatherMap API key not configured"}), 400
    
    results = {}
    for city in cities:
        weather_data = get_weather_data(city, OPEN_WEATHER_API_KEY)
        results[city] = parse_weather_response(weather_data)
    
    return jsonify(results)

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "Weather Dashboard API is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
