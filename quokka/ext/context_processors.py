# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 20:13 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from quokka.core.models.config import Config


def configure(app):
    @app.context_processor
    def inject():
        return dict(
            Config=Config
        )
