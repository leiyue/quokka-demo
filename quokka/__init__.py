# -*- coding: utf-8 -*-
# -*- date: 2016-02-24 21:53 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from quokka.core.admin import create_admin
from quokka.core.app import QuokkaApp
from quokka.ext import configure_extensions

admin = create_admin()


def create_app_base(config=None, test=False, admin_instance=None, **settings):
    app = QuokkaApp(__name__)
    app.config.load_config(config=config, test=test, **settings)

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
    configure_extensions(app, admin_instance or admin)
    return app
