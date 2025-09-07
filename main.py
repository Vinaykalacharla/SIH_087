# main.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

import os
from PIL import Image
import db as db_module
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def current_user_id():
    return session.get('user_id')

@bp.route('/dashboard')
def dashboard():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    # fetch profile summary
    conn = db_module.get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT location, soil_type, crops FROM farmer_profiles WHERE user_id=%s", (uid,))
        profile = cur.fetchone()
        cur.close()
    finally:
        db_module.close_conn(conn)   # ✅ fixed
    return render_template('dashboard.html', profile=profile)

@bp.route('/analytics')
def analytics():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('analytics_dashboard.html')

@bp.route('/weather')
def weather():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('weather.html')

@bp.route('/soil-analysis')
def soil_analysis():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('soil_analysis.html')

@bp.route('/crop-calendar')
def crop_calendar():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('crop_calendar.html')

@bp.route('/market-prices')
def market_prices():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('market_prices.html')

@bp.route('/farm-management')
def farm_management():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('farm_management.html')

@bp.route('/upload-pest', methods=['GET', 'POST'])
def upload_pest():
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '' or not allowed_file(file.filename):
            flash('Valid image required', 'danger')
            return redirect(url_for('main.upload_pest'))

        fname = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        path = os.path.join(UPLOAD_FOLDER, f"{uid}_{fname}")
        file.save(path)

        # Mock detection: pretend we detected an "aphid"
        detected = True
        pest = 'aphid'
        severity = 'low'
        suggested_action = 'Use neem oil spray and monitor weekly.'

        # store into pest_reports
        conn = db_module.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO pest_reports (user_id, image_path, detected, pest, severity, suggested_action) VALUES (%s,%s,%s,%s,%s,%s)",
                (uid, path, detected, pest, severity, suggested_action)
            )
            rid = cur.lastrowid   # ✅ MySQL way to get last inserted ID
            conn.commit()
            cur.close()
        except Exception as e:
            conn.rollback()
            flash('Failed to save report: ' + str(e), 'danger')
            return redirect(url_for('main.upload_pest'))
        finally:
            db_module.close_conn(conn)   # ✅ fixed

        result = {
            'id': rid,
            'image': path,
            'detected': detected,
            'pest': pest,
            'severity': severity,
            'suggested_action': suggested_action
        }
        return render_template('advisory_result.html', result=result)

    return render_template('upload_pest.html')
