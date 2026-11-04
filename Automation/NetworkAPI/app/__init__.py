from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///network.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register route blueprints
    from app.routes.devices import devices_bp
    from app.routes.groups import groups_bp

    app.register_blueprint(devices_bp, url_prefix="/devices")
    app.register_blueprint(groups_bp, url_prefix="/groups")

    # Create database tables
    with app.app_context():
        from app import models
        db.create_all()

    return app