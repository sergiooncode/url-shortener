# -*- coding: utf-8 -*-
import os


BASE_DIR = os.path.dirname(os.path.abspath(__name__))

DEBUG = False
TESTING = False

SQLALCHEMY_DATABASE_URI = "{}{}{}{}".format(
    'sqlite:///',
    BASE_DIR,
    '/',
    'url_shortener.sqlite3'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = "{}:{}".format(
    os.environ.get('SERVER_HOST'),
    os.environ.get('SERVER_PORT')
)
