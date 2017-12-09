# -*- coding: utf-8 -*-
import os
import click
from flask.cli import FlaskGroup

from url_shortener import create_app


def make_app(info):
    return create_app()


@click.group(cls=FlaskGroup, create_app=make_app)
@click.option("--config", expose_value=False, required=False,
              is_flag=False, is_eager=True, metavar="CONFIG",
              help="Specify the config to use in dotted module notation "
              "e.g. url_shortener.config.default.DefaultConfig")
def url_shortener():
    """This is a management script for the url_shortener application."""
    pass


if __name__ == '__main__':
    url_shortener()
