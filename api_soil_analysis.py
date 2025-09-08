from flask import Blueprint, jsonify, session, request
import db as db_module

bp = Blueprint('soil_analysis_api', __name__)

@bp.route('/soil-analysis', methods=['POST'])
def soil_analysis():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    ph_level = data.get('ph_level', 7.0)
    moisture = data.get('moisture', 50)
    nitrogen = data.get('nitrogen', 25)
    phosphorus = data.get('phosphorus', 25)
    potassium = data.get('potassium', 25)

    # Determine nutrient levels
    def get_nutrient_level(value):
        if value < 10:
            return 'Low'
        elif value <= 50:
            return 'Medium'
        else:
            return 'High'

    nutrients = {
        'nitrogen': get_nutrient_level(nitrogen),
        'phosphorus': get_nutrient_level(phosphorus),
        'potassium': get_nutrient_level(potassium)
    }

    # Determine moisture level
    if moisture < 30:
        moisture_level = 'Low'
    elif moisture <= 70:
        moisture_level = 'Adequate'
    else:
        moisture_level = 'High'

    # Generate recommendations
    recommendations = []
    if ph_level < 6.0:
        recommendations.append('Add lime to increase pH level')
    elif ph_level > 7.5:
        recommendations.append('Add sulfur to decrease pH level')
    else:
        recommendations.append('pH level is optimal')

    if nutrients['nitrogen'] == 'Low':
        recommendations.append('Add nitrogen-rich fertilizer')
    if nutrients['phosphorus'] == 'Low':
        recommendations.append('Add phosphorus-rich fertilizer')
    if nutrients['potassium'] == 'Low':
        recommendations.append('Add potassium-rich fertilizer')

    if moisture_level == 'Low':
        recommendations.append('Increase irrigation to raise moisture level')
    elif moisture_level == 'High':
        recommendations.append('Reduce irrigation to lower moisture level')
    else:
        recommendations.append('Maintain current irrigation schedule')

    analysis = {
        'ph_level': ph_level,
        'moisture': f'{moisture}%',
        'nutrients': nutrients,
        'recommendations': recommendations
    }
    return jsonify(analysis)