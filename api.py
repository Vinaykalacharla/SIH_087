# api.py
from flask import Blueprint, request, jsonify, session
import db as db_module

bp = Blueprint('api', __name__)

@bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json() or {}
    user_id = session.get('user_id')  # optional
    crop = data.get('crop', 'wheat')
    soil = data.get('soil', {}).get('type', 'loam')
    # simple heuristic recommendation
    recommendation = f"Balanced NPK fertilizer recommended for {crop} on {soil} soil."
    confidence = 0.55

    # persist
    conn = db_module.get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO recommendations (user_id, crop, soil_type, recommendation, confidence) VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (user_id, crop, soil, recommendation, confidence)
        )
        rec_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_module.close_conn(conn)

    return jsonify({
        'id': rec_id,
        'crop': crop,
        'soil': soil,
        'recommendation': recommendation,
        'confidence': confidence
    })

@bp.route('/api/recommendations/user', methods=['GET'])
def get_user_recommendation():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = db_module.get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT crop, soil_type, recommendation, confidence FROM recommendations WHERE user_id=%s ORDER BY id DESC LIMIT 1",
            (user_id,)
        )
        rec = cur.fetchone()
        cur.close()
    finally:
        db_module.close_conn(conn)

    if not rec:
        return jsonify({'error': 'No recommendations found'}), 404

    crop, soil_type, recommendation, confidence = rec
    return jsonify({
        'crop': crop,
        'soil': soil_type,
        'recommendation': recommendation,
        'confidence': confidence
    })
