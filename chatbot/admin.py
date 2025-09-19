from flask import Blueprint, render_template
from models import ChatSession, ChatMessage

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/')
def admin_index():
    sessions = ChatSession.query.order_by(ChatSession.created_at.desc()).limit(50).all()
    return render_template('admin_index.html', sessions=sessions)

@admin_blueprint.route('/session/<int:sid>')
def view_session(sid):
    session = ChatSession.query.get_or_404(sid)
    messages = ChatMessage.query.filter_by(session_id=sid).order_by(ChatMessage.timestamp.asc()).all()
    return render_template('admin_session.html', session=session, messages=messages)
