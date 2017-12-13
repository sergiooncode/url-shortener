from flask import current_app
from datetime import datetime as dt
from user_agents import parse

from url_shortener.models import MobileRedirect, TabletRedirect, DesktopRedirect, \
    MOBILE_TYPE_STRING, TABLET_TYPE_STRING, DESKTOP_TYPE_STRING


def elapsed_time_in_seconds_since(start_time):
    """
    Calculates the elapsed time between input start_time (expected in UTC) and now in UTC.
    :param start_time, expects datetime.datetime object
    :returns float, elapsed time in seconds
    """
    return (dt.utcnow() - start_time).total_seconds()


def get_device_model_from_device_string(string_):
    device_model = None
    if string_ == MOBILE_TYPE_STRING:
        device_model = MobileRedirect
    elif string_ == TABLET_TYPE_STRING:
        device_model = TabletRedirect
    elif string_ == DESKTOP_TYPE_STRING:
        device_model = DesktopRedirect
    return device_model


def get_device_model_from_request(request):
    """
    Gets the device model class given a request by detecting device based on User-Agent header.
    :param request, Flask request object
    :returns a SQLAlchemy model class
    """
    user_agent = parse(request.headers['User-Agent'])
    device_model = None
    if user_agent.is_mobile:
        device_model = MobileRedirect
    elif user_agent.is_tablet:
        device_model = TabletRedirect
    elif user_agent.is_pc:
        device_model = DesktopRedirect
    else:
        device_model = DesktopRedirect
    return device_model
