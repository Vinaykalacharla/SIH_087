from flask import Blueprint, jsonify, session
import db as db_module

bp = Blueprint('market_prices_api', __name__)

@bp.route('/market-prices', methods=['GET'])
def market_prices():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Mock market prices data
    prices = [
        {'crop': 'Wheat', 'price': 250, 'unit': 'per kg', 'change': '+5%'},
        {'crop': 'Rice', 'price': 180, 'unit': 'per kg', 'change': '-2%'},
        {'crop': 'Corn', 'price': 120, 'unit': 'per kg', 'change': '+3%'},
        {'crop': 'Soybean', 'price': 300, 'unit': 'per kg', 'change': '+1%'},
        {'crop': 'Cotton', 'price': 400, 'unit': 'per kg', 'change': '-4%'}
    ]
    return jsonify(prices)
