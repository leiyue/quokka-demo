# -*- coding: utf-8 -*-
# -*- date: 2016-02-28 12:54 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import importlib
import os


def load_form_folder(app):
    blueprints_path = app.config.get('BLUE_PRINTS_PATH', 'modules')
    path = os.path.join(
        app.config.get(
            'PROJECT_ROOT',
            os.path.join(os.path.dirname(__file__), os.path.pardir)
        ),
        blueprints_path
    )
    base_module_name = '.'.join([app.name, blueprints_path])
    dir_list = os.listdir(path)
    mods = {}
    object_name = app.config.get('BLUEPRINTS_OBJECT_NAME', 'module')
    module_file = app.config.get('BLUEPRINTS_MODULE_NAME', 'main')
    blueprint_module = module_file + '.py'
    for fname in dir_list:
        if not os.path.exists(
                os.path.join(path, fname, 'DISABLED')
        ) and os.path.isdir(
            os.path.join(path, fname)
        ) and os.path.exists(
            os.path.join(path, fname, blueprint_module)
        ):

            module_root = '.'.join([base_module_name, fname])
            module_name = '.'.join([module_root, module_file])
            mods[fname] = importlib.import_module(module_name)
            blueprint = getattr(mods[fname], object_name)
            app.logger.info('Registering blueprint: {0}'.format(blueprint.name))
            app.register_blueprint(blueprint)

            try:
                importlib.import_module('.'.join([module_root, 'admin']))
            except ImportError as e:
                app.logger.info(
                    '%s module does not define admin or error: %s', fname, e
                )
    app.logger.info('%s modules loaded', mods.keys())
