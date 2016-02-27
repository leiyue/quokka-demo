# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 19:45 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.mistune import Mistune


def configure(app):
    Mistune(app)
    if app.config.get('GRAVATAR'):
        from flask.ext.gravatar import Gravatar
        Gravatar(app, **app.config.get('GRAVATAR'))
