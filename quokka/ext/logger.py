# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 14:19 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging


def configure(app):
    app.logger.setLevel(logging.DEBUG)
