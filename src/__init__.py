# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# db = SQLAlchemy()
# login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__,
#                 template_folder='src/ui',
#                 static_folder='assets')
    
#     # Configuration
#     app.config['SECRET_KEY'] = 'weoho ghr4e'
#     #app.config['SQLCHEMY_DATABASE_URI'] = 'sqlite:///data/budget.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    # db.init_app(app)
    # login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'

    # # Import and register blueprints
    # from .core.auth import sign_up
    # from .core.transactions import transactions
    
    # app.register_blueprint(auth)
    # app.register_blueprint(transactions)

    #return app
