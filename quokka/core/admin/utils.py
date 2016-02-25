# -*- coding: utf-8 -*-
# -*- date: 2016-02-26 0:29 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask.ext.admin.babel import ngettext, lazy_gettext, gettext


def _(*args, **kwargs):
    return gettext(*args, **kwargs)


def _l(*args, **kwargs):
    return lazy_gettext(*args, **kwargs)


def _n(*args, **kwargs):
    return ngettext(*args, **kwargs)
