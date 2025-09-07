from flask import Blueprint, jsonify, session
import db as db_module

bp = Blueprint('analytics_api', __name__)

@bp.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = db_module.get_conn()
    try:
        cur = conn.cursor()
        # Fetch yield data
        cur.execute("""
            SELECT year, month, SUM(yield) as total_yield
            FROM farm_yield
            WHERE user_id=%s
            GROUP BY year, month
            ORDER BY year, month
        """, (user_id,))
        yield_data = cur.fetchall()

        # Fetch revenue data
        cur.execute("""
            SELECT year, month, SUM(revenue) as total_revenue
            FROM farm_revenue
            WHERE user_id=%s
            GROUP BY year, month
            ORDER BY year, month
        """, (user_id,))
        revenue_data = cur.fetchall()

        # Fetch goals data
        cur.execute("""
            SELECT year, month, target_yield, target_revenue
            FROM farm_goals
            WHERE user_id=%s
            ORDER BY year, month
        """, (user_id,))
        goals_data = cur.fetchall()

        cur.close()
    finally:
        db_module.close_conn(conn)

    return jsonify({
        'yield': yield_data,
        'revenue': revenue_data,
        'goals': goals_data
    })
