# -*- coding: utf-8 -*-
# -*- date: 2016-02-26 0:29 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging

from flask import session, request
from flask.ext.admin import Admin
from flask.ext.admin.contrib.mongoengine import ModelView

logger = logging.getLogger()


class QuokkaAdmin(Admin):
    registered = []

    def register(self, model, view=None, *args, **kwargs):
        _view = view or ModelView
        identifier = '.'.join((model.__module__, model.__name__))
        if identifier not in self.registered:
            self.add_view(_view(model, *args, **kwargs))
            self.registered.append(identifier)
        logger.debug(identifier)


def create_admin(app=None):
    return QuokkaAdmin(app)


def configure_admin(app, admin):
    babel = app.extensions.get('babel')
    if babel:
        try:
            @babel.localeselector
            def get_locale():
                # use default language if set
                if app.config.get('BABEL_DEFAULT_LOCALE'):
                    session['lang'] = app.config.get('BABEL_DEFAULT_LOCALE')
                else:
                    # get best matching language
                    if app.config.get('BABEL_LANGUAGES'):
                        session['lang'] = request.accept_languages.best_match(
                            app.config.get('BABEL_LANGUAGES')
                        )

                return session.get('lang', 'en')

            admin.locale_selector(get_locale)
            app.logger.info(session.get('lang'))
        except Exception as e:
            app.logger.info('Cannot add locale_selector. %s' % e)

            if admin.app is None:
                admin.init_app(app)

    return admin
