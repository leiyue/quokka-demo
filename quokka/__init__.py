# -*- coding: utf-8 -*-
# -*- date: 2016-02-24 21:53 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .core import QuokkaApp
from .ext import configure_extensions


def create_app_base(config=None, test=False, admin_instance=None, **settings):
    app = QuokkaApp(__name__)
    app.config.from_yaml('settings.yaml')

    app.config['MONGODB_SETTINGS'] = {
        'db': 'quokka_dev',
        'host': 'localhost',
        'port': 27017
    }

    if test or app.config.get('TESTING'):
        app.testing = True

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app


def create_app(config=None, test=False, admin_instance=None, **settings):
    app = create_app_base(
        config=config, test=test, admin_instance=admin_instance, **settings
    )
    configure_extensions(app)
    return app
