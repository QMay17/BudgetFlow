from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")