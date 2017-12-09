# -*- coding: utf-8 -*-
from url_shortener.config.default import DefaultConfig


class TestingConfig(DefaultConfig):

    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        'sqlite://'
    )
