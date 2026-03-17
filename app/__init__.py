from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.inquiries import inquiries_bp
    from app.routes.reminders import reminders_bp
    from app.routes.sessions import sessions_bp
    from app.routes.payments import payments_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inquiries_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(dashboard_bp)
    return app
