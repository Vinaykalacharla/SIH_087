# app.py
from flask import Flask, render_template
from config import Config
import db as db_module

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # No init_pool() needed for PyMySQL

    # import route modules
    import auth
    import main
    import api
    import admin
    import api_analytics
    import api_weather
    import api_crop_calendar
    import api_soil_analysis
    import api_market_prices
    import api_farm_management

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(api_analytics.bp, url_prefix='/api')
    app.register_blueprint(api_weather.bp, url_prefix='/api')
    app.register_blueprint(api_crop_calendar.bp, url_prefix='/api')
    app.register_blueprint(api_soil_analysis.bp, url_prefix='/api')
    app.register_blueprint(api_market_prices.bp, url_prefix='/api')
    app.register_blueprint(api_farm_management.bp, url_prefix='/api')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/ai-recommendation')
    def ai_recommendation():
        return render_template('ai_recommendation.html')

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
