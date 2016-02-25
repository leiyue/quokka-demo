# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 22:13 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.script import Manager
from flask.ext.script.commands import Shell, Server, Clean, ShowUrls

from quokka import create_app
from quokka.core import db, models
from quokka.utils import Populate

app = create_app()
manager = Manager(app)


@manager.command
def populate():
    Populate(db=db)


def _make_context():
    return dict(app=app, db=db, models=models)


manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('runserver', Server(port=app.config.get('PORT', 5000)))
manager.add_command('public', Server(port=app.config.get('PORT', 5000), host='0.0.0.0'))
manager.add_command('clean', Clean)
manager.add_command('urls', ShowUrls)

if __name__ == '__main__':
    with app.app_context():
        manager.run()
