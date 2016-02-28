# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 19:34 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.babel import Babel

babel = Babel()


def configure(app):
    babel.init_app(app)
