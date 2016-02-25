# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 23:01 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.mongoengine import MongoEngineSessionInterface

from ..core import db


def configure_extensions(app):
    db.init_app(app)
    app.session_interface = MongoEngineSessionInterface(db)
    return app


def configure_extensions_min(app):
    db.init_app(app)
    return app
