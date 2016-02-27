# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 19:50 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from quokka_themes import Themes

themes = Themes()


def configure(app):
    themes.init_themes(app, app_identifier='quokka')
