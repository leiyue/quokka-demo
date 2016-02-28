# -*- coding: utf-8 -*-
# -*- date: 2016-02-26 0:29 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging

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
    if admin.app is None:
        admin.init_app(app)

    return admin
