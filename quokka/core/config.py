# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 22:22 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging
import os

import yaml
from flask import Config

logger = logging.getLogger()


class QuokkaConfig(Config):
    def from_yaml(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)

        with open(filename) as config_file:
            c = yaml.load(config_file)

        env = os.environ.get('FLASK_ENV', 'DEVELOPMENT').upper()
        self['ENVIRONMENT'] = env.lower()

        c = c.get(env, c)
        self.update(c)
