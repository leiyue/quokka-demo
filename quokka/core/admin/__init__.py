# -*- coding: utf-8 -*-
# -*- date: 2016-02-26 0:29 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.admin import Admin
from flask.ext.admin.contrib.pymongo import ModelView


def create_admin(app=None):
    return Admin()


def configure_admin(app, admin):
    # from quokka.models import Role

    # admin.add_view(ModelView(Role, category='系统管理', name='配置管理'))
    # admin.add_view(ModelView(User, category='系统管理', name='配置管理'))

    if admin.app is None:
        admin.init_app(app)

    return admin
