from flask import Blueprint, jsonify, request, session
import requests
from config import Config

bp = Blueprint('weather_api', __name__)

@bp.route('/current', methods=['GET'])
def current_weather():
    # Temporarily removed authentication for testing
    # user_id = session.get('user_id')
    # if not user_id:
    #     return jsonify({'error': 'Unauthorized'}), 401

    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400

    api_key = Config.WEATHER_API_KEY
    if not api_key:
        return jsonify({'error': 'Weather API key not configured'}), 500

    # Get current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location},IN&appid={api_key}&units=metric"
    try:
        print(f"Received current weather request for location: {location}")
        resp = requests.get(url)
        data = resp.json()
        if resp.status_code != 200:
            return jsonify({'error': data.get('message', 'Failed to fetch weather')}), resp.status_code

        weather_data = {
            'location': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'condition': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
        return jsonify(weather_data)
    except Exception as e:
        print(f"Exception in current_weather: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/forecast', methods=['GET'])
def weather_forecast():
    # Temporarily removed authentication for testing
    # user_id = session.get('user_id')
    # if not user_id:
    #     return jsonify({'error': 'Unauthorized'}), 401

    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400

    api_key = Config.WEATHER_API_KEY
    if not api_key:
        return jsonify({'error': 'Weather API key not configured'}), 500

    # Get coordinates for location using OpenWeatherMap Geocoding API
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location},IN&limit=1&appid={api_key}"
    try:
        print(f"Received forecast request for location: {location}")  # Added log
        geo_resp = requests.get(geo_url)
        geo_data = geo_resp.json()
        print(f"Geocoding API response for location '{location}': {geo_data}")  # Debug log
        if not geo_data:
            return jsonify({'error': f"Location '{location}' not found"}), 404
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Get 7-day forecast using One Call API 3.0
        forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}&units=metric"
        forecast_resp = requests.get(forecast_url)
        forecast_data = forecast_resp.json()
        print(f"One Call API response: {forecast_data}")  # Added log
        if forecast_resp.status_code != 200:
            return jsonify({'error': forecast_data.get('message', 'Failed to fetch forecast')}), forecast_resp.status_code

        daily_forecasts = []
        for day in forecast_data.get('daily', [])[:7]:
            daily_forecasts.append({
                'date': day['dt'],
                'temp_day': day['temp']['day'],
                'temp_night': day['temp']['night'],
                'humidity': day['humidity'],
                'wind_speed': day['wind_speed'],
                'condition': day['weather'][0]['description'],
                'icon': day['weather'][0]['icon']
            })

        return jsonify({
            'location': location,
            'daily_forecasts': daily_forecasts
        })
    except Exception as e:
        print(f"Exception in weather_forecast: {e}")  # Debug log
        return jsonify({'error': str(e)}), 500
