from flask import Flask

from config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from app.routes import api

    app.register_blueprint(
        api,
        url_prefix="/api"
    )

    # Register error handlers
    from app.errors import register_error_handlers

    register_error_handlers(app)

    return app