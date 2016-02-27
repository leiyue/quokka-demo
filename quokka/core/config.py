# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 22:22 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging
import os

import yaml
from cached_property import cached_property
from flask import Config

logger = logging.getLogger()


class QuokkaConfig(Config):
    @cached_property
    def store(self):
        return dict(self)

    def from_yaml(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        try:
            with open(filename) as config_file:
                c = yaml.load(config_file)
        except Exception as e:
            if silent:
                return False
            e.message = 'Unable to load ymal configuration: {0}'.format(
                filename
            )
            raise
        env = os.environ.get('FLASK_ENV', 'DEVELOPMENT').upper()
        self['ENVIRONMENT'] = env.lower()

        c = c.get(env, c)
        self.update(c)

    def from_database(self, models, silent=False):
        if models:
            try:
                c = {
                    item.name: item.value
                    for item in models.Config.objects.get(group='settings').values
                    }
                self.update(c)
            except Exception as e:
                if silent:
                    return False
                logger.warning('Error reading settings from models: {0}'.format(e))
                raise

    def to_database(self, models, silent=False):
        if models:
            # try:
            c = dict(self)
            print(id(logger))
            logger.info(c)

            s = models.Config.objects.get(group='settings').values
            logger.info(s[0].name)


            # except Exception as e:
            #     if silent:
            #         return False
            #     logger.warning('Error writing settings to models: {0}'.format(e))
