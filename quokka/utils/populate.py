# -*- coding: utf-8 -*-
# -*- date: 2016-02-26 0:58 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import json
import logging

from ..core.models import Config, CustomValue

logger = logging.getLogger()


class Populate(object):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        self.args = args
        self.kwargs = kwargs
        self.json_data = {}
        self.configs_data = {}
        self.custom_values = {}
        self.load_fixtures()
        self.app = self.kwargs.get('app')

    def __call__(self, *args, **kwargs):
        self.pipeline()

    def pipeline(self):
        self.create_configs()

    def load_fixtures(self):
        file_path = self.kwargs.get(
            'file-path',
            './etc/fixtures/initial_data.json'
        )
        _file = open(file_path)
        self.json_data = json.load(_file)

    def custom_value(self, **data):
        if data.get('name') in self.custom_values:
            return self.custom_values[data.get('name')]

        value = CustomValue(**data)
        self.custom_values[value.name] = value
        return value

    @staticmethod
    def create_config(data):
        try:
            return Config.objects.get(group=data.get('group'))
        except:
            return Config.objects.create(**data)

    def create_configs(self):
        self.configs_data = self.json_data.get('configs')

        for config in self.configs_data:
            config['values'] = [self.custom_value(**args)
                                for args in config.get('values')]
            self.create_config(config)
