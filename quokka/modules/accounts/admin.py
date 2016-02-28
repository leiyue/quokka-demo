# -*- coding: utf-8 -*-
# -*- date: 2016-02-28 11:50 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.admin.contrib.mongoengine import ModelView

from quokka import admin
from quokka.core.admin.utils import _l
from quokka.modules.accounts.models import Role


class RoleAdmin(ModelView):
    pass


admin.register(Role, RoleAdmin, category=_l('Accounts'), name=_l('Roles'))
