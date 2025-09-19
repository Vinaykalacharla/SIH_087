from .extensions import db
from datetime import datetime

# This file will only hold models we define in Flask.
# Your MySQL already has other tables (users, admins, etc.),
# so we only add ChatLog here to not overwrite existing data.

class ChatLog(db.Model):
    __tablename__ = "chat_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)  # can link to users table if needed
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
