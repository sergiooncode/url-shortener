# -*- coding: utf-8 -*-
import os


class DefaultConfig:

    basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                           os.path.dirname(__file__)))))

    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "{}{}{}{}".format(
        'sqlite:///',
        basedir,
        '/',
        'url_shortener.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
