from flask import Flask, render_template
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize DB
    db.init_app(app)

    # Register blueprints
    from chatbot import chatbot_bp
    app.register_blueprint(chatbot_bp)

    with app.app_context():
        db.create_all()  # ensures chat_logs table is created

    # Basic route
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
