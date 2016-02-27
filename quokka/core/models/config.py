# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 23:27 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask import current_app

from quokka.core.fields import MultipleObjectsReturned
from .custom_values import HasCustomValue
from .. import db


class Config(HasCustomValue, db.DynamicDocument):
    group = db.StringField(max_length=255)
    description = db.StringField()

    @classmethod
    def get(cls, group, name=None, default=None):
        try:
            instance = cls.objects.get(group=group)
        except:
            return None

        if not name:
            ret = instance.values
            if group == 'settings':
                ret = {}
                ret.update(current_app.config)
                ret.update({item.name: item.value for item in instance.values})
        else:
            try:
                ret = instance.values.get(name=name).value
            except (MultipleObjectsReturned, AttributeError):
                ret = None
        if not ret and group == 'settings' and name is not None:
            ret = current_app.config.store.get(name)

        return ret or default

    def __unicode__(self):
        return self.group
