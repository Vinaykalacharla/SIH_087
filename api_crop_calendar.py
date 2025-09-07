from flask import Blueprint, jsonify, session
import db as db_module

bp = Blueprint('crop_calendar_api', __name__)

@bp.route('/crop-calendar', methods=['GET'])
def crop_calendar():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Mock crop calendar data
    calendar = [
        {'month': 'January', 'activities': ['Prepare soil', 'Plant winter crops']},
        {'month': 'February', 'activities': ['Fertilize', 'Monitor pests']},
        {'month': 'March', 'activities': ['Plant spring crops', 'Irrigate']},
        {'month': 'April', 'activities': ['Weed control', 'Harvest early crops']},
        {'month': 'May', 'activities': ['Plant summer crops', 'Pest control']},
        {'month': 'June', 'activities': ['Irrigate regularly', 'Monitor growth']},
        {'month': 'July', 'activities': ['Harvest summer crops', 'Prepare for fall']},
        {'month': 'August', 'activities': ['Fertilize', 'Pest monitoring']},
        {'month': 'September', 'activities': ['Plant fall crops', 'Harvest']},
        {'month': 'October', 'activities': ['Soil preparation', 'Weed control']},
        {'month': 'November', 'activities': ['Winterize crops', 'Monitor weather']},
        {'month': 'December', 'activities': ['Rest period', 'Plan next season']}
    ]
    return jsonify(calendar)
