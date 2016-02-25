# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 23:27 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from .custom_values import HasCustomValue
from .. import db


class Config(HasCustomValue, db.DynamicDocument):
    group = db.StringField(max_length=255)
    description = db.StringField()

    def __unicode__(self):
        return self.group
