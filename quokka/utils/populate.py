# -*- coding: utf-8 -*-
# -*- date: 2016-02-26 0:58 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import json
import logging

from quokka.models import User, Role
from ..core.models import Config, CustomValue

logger = logging.getLogger()


class Populate(object):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        self.args = args
        self.kwargs = kwargs
        self.roles = {}
        self.users = {}
        self.custom_values = {}
        self.load_fixtures()
        self.app = self.kwargs.get('app')

    def __call__(self, *args, **kwargs):
        self.pipeline()

    def pipeline(self):
        self.create_users()
        self.create_configs()

    def load_fixtures(self):
        file_path = self.kwargs.get(
            'file-path',
            './etc/fixtures/initial_data.json'
        )
        _file = open(file_path)
        self.json_data = json.load(_file)

    def role(self, name):
        if name not in self.roles:
            try:
                role = Role.objects.get(name=name)
            except Role.DoesNotExist:
                role = Role.objects.create(name=name)
                logger.info('Created: Role {0}'.format(name))
            self.roles[name] = role
        return self.roles.get(name)

    def create_user(self, data):
        name = data.get('name')
        if name not in self.users:
            pwd = data.get('password')
            data['roles'] = [self.role(role) for role in data.get('roles')]
            user = User.create_user(**data)
            logger.info('Created: User: {0} {1}'.format(user.email, pwd))
            return user

    def create_users(self, data=None):
        self.users_data = data or self.json_data.get('users')
        for user in self.users_data:
            self.create_user(user)

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
