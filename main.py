from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db as db_module

bp = Blueprint('main', __name__)

def current_user_id():
    return session.get('user_id')

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Handles user profile updates and display."""
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))

    conn = db_module.get_conn()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        language = request.form.get('language')  # Consider a select field for controlled vocabulary

        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET name=%s, email=%s, role=%s, language=%s WHERE id=%s",
                (name, email, role, language, uid)
            )
            conn.commit()
            cur.close()
            flash('Profile updated successfully', 'success')
        except Exception as e:
            conn.rollback()
            flash('Failed to update profile: ' + str(e), 'danger')
        finally:
            if conn:  # Ensure connection is valid before closing
                db_module.close_conn(conn)
        return redirect(url_for('main.dashboard'))

    # GET request: fetch current profile data
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, email, role, language FROM users WHERE id=%s", (uid,))
        profile = cur.fetchone()
        cur.close()
    finally:
        if conn:  # Ensure connection is valid before closing
            db_module.close_conn(conn)

    return render_template('profile.html', profile=profile)

@bp.route('/advisory-result')
def advisory_result():
    """Protects the advisory result route."""
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    # You may want to pass a result to the advisory page, if that's the case add `result=result`
    return render_template('advisory_result.html')

@bp.route('/dashboard')
def dashboard():
    """Protects the dashboard route."""
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@bp.route('/weather')
def weather():
    """Protects the weather route."""
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('weather.html')

@bp.route('/analytics')
def analytics():
    """Protects the analytics route."""
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('analytics_dashboard.html')

@bp.route('/crop-calendar')
def crop_calendar():   # 🐛 missing docstring
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('crop_calendar.html')

@bp.route('/soil-analysis')
def soil_analysis():    # 🐛 missing docstring
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('soil_analysis.html')

@bp.route('/market-prices')
def market_prices():    # 🐛 missing docstring
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('market_prices.html')

@bp.route('/farm-management')
def farm_management():  # 🐛 missing docstring
    uid = current_user_id()
    if not uid:
        return redirect(url_for('auth.login'))
    return render_template('farm_management.html')


import os  # Import os at the top of the file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'  # Define UPLOAD_FOLDER outside the function
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Define allowed extensions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload-pest', methods=['GET', 'POST'])
def upload_pest():
    """Handles pest image uploads and analysis."""
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
        path = os.path.join(UPLOAD_FOLDER, f"{uid}_{fname}")  # Use secure_filename
        file.save(path)

        # Mock detection: pretend we detected an "aphid"
        detected = True
        pest = 'aphid'
        severity = 'low'
        suggested_action = 'Use neem oil spray and monitor weekly.'  # Replace with dynamic result

        # store into pest_reports
        conn = db_module.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO pest_reports (user_id, image_path, detected, pest, severity, suggested_action) VALUES (%s,%s,%s,%s,%s,%s)",
                (uid, path, detected, pest, severity, suggested_action)  # Correct order
            )
            rid = cur.lastrowid   # ✅ MySQL way to get last inserted ID
            conn.commit()
            cur.close()
        except Exception as e:
            conn.rollback()
            flash('Failed to save report: ' + str(e), 'danger')
            return redirect(url_for('main.upload_pest'))
        finally:
            db_module.close_conn(conn)

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
