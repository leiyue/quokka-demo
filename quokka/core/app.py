# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 22:19 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from flask import Flask

from .config import QuokkaConfig


class QuokkaApp(Flask):
    config_class = QuokkaConfig

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return self.config_class(root_path, self.default_config)
