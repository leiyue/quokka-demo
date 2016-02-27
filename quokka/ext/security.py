# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 20:18 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.security import MongoEngineUserDatastore
from flask.ext.security import Security


def configure(app, db):
    from ..models import User, Role
    app.security = Security(
        app=app,
        datastore=MongoEngineUserDatastore(db, User, Role),
    )
