from flask import Flask, render_template
from config import Config
from models.database import db
from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp
from routes.report_routes import report_bp
from routes.budget_routes import budget_bp

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='templates',  # Changed from 'ui' to 'templates'
                static_folder='../assets')
    
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(budget_bp)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return render_template('main_window.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)