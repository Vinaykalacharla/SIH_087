# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import db as db_module

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not (email and password):
            flash('Email and password are required', 'danger')
            return render_template('register.html')

        # Hash the password
        pw_hash = generate_password_hash(password)

        conn = db_module.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, pw_hash)
            )
            conn.commit()
            cur.close()

            # auto-login: fetch user id
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE email=%s", (email,))
            row = cur.fetchone()
            cur.close()

            if row:
                session['user_id'] = row['id'] if isinstance(row, dict) else row[0]
                return redirect(url_for('main.dashboard'))

        except Exception as e:
            conn.rollback()
            flash('Registration failed: ' + str(e), 'danger')
            return render_template('register.html')
        finally:
            db_module.close_conn(conn)

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = db_module.get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, password_hash FROM users WHERE email=%s", (email,))
            row = cur.fetchone()
            cur.close()

            if row:
                user_id = row['id'] if isinstance(row, dict) else row[0]
                stored_hash = row['password_hash'] if isinstance(row, dict) else row[1]

                if check_password_hash(stored_hash, password):
                    session['user_id'] = user_id
                    return redirect(url_for('main.dashboard'))

            flash('Invalid email or password', 'danger')

        finally:
            db_module.close_conn(conn)

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
