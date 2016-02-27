# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 21:49 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from slugify import slugify as awesome_slugify


def slugify(text):
    return awesome_slugify(text).lower()
