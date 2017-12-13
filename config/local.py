# -*- coding: utf-8 -*-
import os


BASE_DIR = os.path.dirname(os.path.abspath(__name__))

DEBUG = False
TESTING = False

SQLALCHEMY_DATABASE_URI = "{}{}/{}".format(
    'sqlite:///',
    BASE_DIR,
    'url_shortener.sqlite3'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

APP_HOST = os.environ.get('APP_HOST')
APP_PORT = os.environ.get('APP_PORT')

API_VERSION = 'v1'
