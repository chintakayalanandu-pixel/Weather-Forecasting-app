import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def get_weather():
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=zh_cn"
    elif city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_cn"
    else:
        return jsonify({"error": "Please provide a city or coordinates"}), 400

    resp = requests.get(url)
    if resp.status_code != 200:
        return jsonify({"error": "City not found or API key is not working"}), 404

    data = resp.json()
    result = {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"]
    }
    return jsonify(result)


@app.route("/api/forecast")
def get_forecast():
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    elif city:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    else:
        return jsonify({"error": "Please provide a city or coordinates"}), 400

    resp = requests.get(url)
    if resp.status_code != 200:
        return jsonify({"error": "Forecast data not found"}), 404

    data = resp.json()
    items = data["list"][::8]
    result = []
    for item in items:
        result.append({
            "time": item["dt_txt"],
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"]
        })
    return jsonify(result)


@app.route("/api/hourly")
def get_hourly():
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    elif city:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    else:
        return jsonify({"error": "Please provide a city or coordinates"}), 400

    resp = requests.get(url)
    if resp.status_code != 200:
        return jsonify({"error": "Hourly data not found"}), 404

    data = resp.json()
    items = data["list"][:8]
    result = []
    for item in items:
        result.append({
            "time": item["dt_txt"],
            "temp": item["main"]["temp"],
            "icon": item["weather"][0]["icon"],
            "description": item["weather"][0]["description"]
        })
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
