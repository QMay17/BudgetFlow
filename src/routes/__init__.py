def register_all_blueprints(app):
    from .auth_routes import bp as auth_bp
    from .transaction_routes import bp as transaction_bp
    from .report_routes import bp as report_bp
    from .budget_routes import bp as budget_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(budget_bp)
    
    return app