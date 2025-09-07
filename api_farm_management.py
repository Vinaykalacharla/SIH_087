from flask import Blueprint, jsonify, session, request
import db as db_module

bp = Blueprint('farm_management_api', __name__)

@bp.route('/farm-management', methods=['GET', 'POST'])
def farm_management():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    if request.method == 'POST':
        # Update farm profile
        data = request.get_json()
        location = data.get('location')
        soil_type = data.get('soil_type')
        crops = data.get('crops')
        conn = db_module.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO farmer_profiles (user_id, location, soil_type, crops) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE location=%s, soil_type=%s, crops=%s",
                (user_id, location, soil_type, crops, location, soil_type, crops)
            )
            conn.commit()
            cur.close()
        finally:
            db_module.close_conn(conn)
        return jsonify({'message': 'Farm profile updated'})

    # Get current profile
    conn = db_module.get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT location, soil_type, crops FROM farmer_profiles WHERE user_id=%s", (user_id,))
        profile = cur.fetchone()
        cur.close()
    finally:
        db_module.close_conn(conn)
    return jsonify(profile or {})
