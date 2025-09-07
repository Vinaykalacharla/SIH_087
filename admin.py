# admin.py
from flask import Blueprint, render_template, session, redirect, url_for
import db as db_module

bp = Blueprint('admin', __name__)

def is_admin():
    uid = session.get('user_id')
    if not uid:
        return False
    conn = db_module.get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT is_super FROM admins WHERE user_id=%s", (uid,))
        row = cur.fetchone()
        cur.close()
        return row is not None and row[0] is True
    finally:
        db_module.close_conn(conn)

@bp.route('/')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('auth.login'))
    conn = db_module.get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT u.id, u.name, u.email, u.created_at FROM users u ORDER BY u.created_at DESC LIMIT 100")
        users = cur.fetchall()
        cur.close()
    finally:
        db_module.close_conn(conn)
    return render_template('admin_dashboard.html', users=users)
