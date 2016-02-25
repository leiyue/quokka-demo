# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 23:09 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.mongoengine import MongoEngine

from .fields import ListField

db = MongoEngine()
db.ListField = ListField
