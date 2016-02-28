# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 23:01 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from quokka.core.admin import configure_admin
from quokka.core.cache import cache
from quokka.core.db import db
from . import (logger, babel, themes, context_processors, security, blueprints)


def configure_extensions(app, admin):
    logger.configure(app)
    cache.init_app(app)
    babel.configure(app)
    db.init_app(app)
    themes.configure(app)
    context_processors.configure(app)
    security.configure(app, db)
    configure_admin(app, admin)
    blueprints.load_form_folder(app)
    return app


def configure_extensions_min(app):
    db.init_app(app)
    security.configure(app, db)
    return app
