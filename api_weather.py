import requests
from flask import Blueprint, jsonify, request, session
from config import Config

bp = Blueprint('weather_api', __name__)

@bp.route('/weather/current', methods=['GET'])
def current_weather():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # For demo, get location from query param or default
    location = request.args.get('location', 'New York')

    # Use a weather API, e.g. OpenWeatherMap
    api_key = Config.WEATHER_API_KEY
    if not api_key:
        return jsonify({'error': 'Weather API key not configured'}), 500

    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        resp = requests.get(url)
        data = resp.json()
        if resp.status_code != 200:
            return jsonify({'error': data.get('message', 'Failed to fetch weather')}), resp.status_code

        weather_info = {
            'location': location,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'condition': data['weather'][0]['description'],
            'uv_index': None  # Could be fetched from another API endpoint if needed
        }
        return jsonify(weather_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
