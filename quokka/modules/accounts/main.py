# -*- coding: utf-8 -*-
# -*- date: 2016-02-28 22:39 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from quokka.core.app import QuokkaModule

module = QuokkaModule('accounts', __name__, template_folder='templates')
