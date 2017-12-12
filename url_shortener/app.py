# -*- coding: utf-8 -*-
import os
from flask import Flask

from url_shortener.api.v1.views import api_v1
from url_shortener.models import db
from url_shortener.hashing import Base62_Hasher

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


def create_app():
    """
    URL Shortener application factory
    """

    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    app.app_context().push()
    configure_blueprints(app)
    initialize_db()
    initialize_hasher(app)

    return app


def configure_app(app):
    """Configures url_shortener."""
    if os.environ.get('URL_SHORTENER_SETTINGS'):
        app.config.from_envvar('URL_SHORTENER_SETTINGS')
        return
    default_config_path = "{}{}".format(
        BASE_DIR,
        '/config/local.py'
    )
    app.config.from_pyfile(default_config_path)


def configure_blueprints(app):
    app.register_blueprint(api_v1)


def initialize_db():
    db.create_all()


def initialize_hasher(app):
    """
    Sets up hashing mechanism necessary for the mapping long url to short url
    """
    app.hasher = Base62_Hasher()
