from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.estoque import estoque_bp
    from routes.vendas import vendas_bp
    from routes.analise import analise_bp
    from routes.devedores import devedores_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(analise_bp)
    app.register_blueprint(devedores_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
