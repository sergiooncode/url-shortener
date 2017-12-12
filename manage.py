#!/usr/bin/env python
from flask_script import Manager

from url_shortener import create_app
from url_shortener.models import db

app = create_app()
manager = Manager(app)


@manager.shell
def make_shell_context():
    return {'app': app, 'db': db}


if __name__ == '__main__':
    manager.run()
