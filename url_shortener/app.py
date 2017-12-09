# -*- coding: utf-8 -*-
from flask import Flask

from url_shortener.database import init_db
from url_shortener.api.v1.views import api_v1


def create_app(config=None):
    app = Flask(__name__)
    configure_app(app, config)
    configure_blueprints(app)
    initialize_db(app)

    return app


def configure_app(app, config):
    """Configures url_shortener."""
    app.config.from_object('url_shortener.config.default.DefaultConfig')


def configure_blueprints(app):
    app.register_blueprint(api_v1)


def initialize_db(app):
    init_db()
