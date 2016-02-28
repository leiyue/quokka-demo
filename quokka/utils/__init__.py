# -*- coding: utf-8 -*-
# -*- date: 2016-02-26 0:58 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging

logger = logging.getLogger()


def lazy_setting(key, default=None):
    from speaklater import make_lazy_string
    from flask import current_app
    return make_lazy_string(
        lambda: current_app.config.get(key, default)
    )


def lazy_str_setting(key, default=None):
    return str(lazy_setting(key, default))


def get_current_user():
    from quokka.modules.accounts.models import User
    from flask.ext.security import current_user

    try:
        return User.objects.get(id=current_user.id)
    except Exception as e:
        logger.warning('No user found: {0}'.format(e))
        return current_user


def get_current_user_for_models():
    user = get_current_user()
    try:
        if not user.is_authenticated():
            return None
        return user
    except Exception as e:
        logger.info('Can not access is_authenticated method: {0}'.format(e))
        return None


def is_accessible(roles_accepted=None, user=None):
    user = user or get_current_user()
    if user.has_role('admin'):
        return True
    if roles_accepted:
        accessible = any(user.has_role(role) for role in roles_accepted)
        return accessible
    return True


def parse_conf_data(data):
    import json
    true_values = ('1', 'enable', 'on', 't', 'true', 'y', 'yes')
    converters = {
        '@int': int,
        '@float': float,
        '@bool': lambda value: True if value.lower() in true_values else False,
        '@json': json.loads
    }

    if data.startswith(tuple(converters.keys())):
        parts = data.partition(' ')
        converter_key = parts[0]
        value = parts[-1]
        return converters.get(converter_key)(value)
    return data
