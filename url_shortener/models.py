# -*- coding: utf-8 -*-
from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

db = SQLAlchemy()

MOBILE_TYPE_STRING = 'mobile'
TABLET_TYPE_STRING = 'tablet'
DESKTOP_TYPE_STRING = 'desktop'


class Redirect(db.Model):

    __tablename__ = 'redirect'

    id = Column(Integer, primary_key=True)
    hashed_id = Column(String(255), default='', index=True)
    long_url = Column(String(1024))
    redirect_count = Column(Integer, default=0)
    type = Column(String(20))
    created_at = Column(DateTime, default=dt.utcnow)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return "<Redirect(id={}, long_url={}, hashed_id={}, type={}, redirect_count={})>".format(
            self.id, self.long_url, self.hashed_id, self.type, self.redirect_count
        )

    __mapper_args__ = {
        'polymorphic_on': type
    }  


class MobileRedirect(Redirect):

    __mapper_args__ = {
        'polymorphic_identity': MOBILE_TYPE_STRING
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs, type=MOBILE_TYPE_STRING)


class TabletRedirect(Redirect):

    __mapper_args__ = {
        'polymorphic_identity': TABLET_TYPE_STRING
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs, type=TABLET_TYPE_STRING)


class DesktopRedirect(Redirect):

    __mapper_args__ = {
        'polymorphic_identity': DESKTOP_TYPE_STRING
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs, type=DESKTOP_TYPE_STRING)
