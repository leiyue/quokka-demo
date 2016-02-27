# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 22:22 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging
import os

import yaml
from cached_property import cached_property, cached_property_ttl
from flask import Config

logger = logging.getLogger()


class QuokkaConfig(Config):
    @cached_property
    def store(self):
        return dict(self)

    @cached_property_ttl(300)
    def settings_from_database(self):

        try:
            import quokka.core.models as m

            return {item.name: item.value
                    for item in m.Config.objects.get(group='settings').values
                    }
        except Exception as e:
            logger.warning('Error reading setting form db: {0}'.format(e))
            return {}

    def get_settings(self, key, default=None):
        return self.settings_from_database.get(key, default)

    def __getitem__(self, key):
        return self.get_settings(key) or dict.__getitem__(self, key)

    def get(self, key, default=None):
        return self.get_settings(key) or self.store.get(key) or default

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

    def load_config(self, config=None, **settings):
        self.from_yaml('../etc/conf/settings.yaml')
        self.from_object(config or 'quokka.settings')
        self.update(settings)
