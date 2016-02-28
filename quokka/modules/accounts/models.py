# -*- coding: utf-8 -*-
# -*- date: 2016-02-27 20:21 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging
import random

from flask.ext.security import RoleMixin, UserMixin
from flask.ext.security.utils import encrypt_password

from quokka.core.db import db
from quokka.utils.text import slugify

logger = logging.getLogger()


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    @classmethod
    def create_role(cls, name, description=None):
        return cls.objects.create(
            name=name,
            description=description
        )

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.description or 'Role')


class UserLink(db.EmbeddedDocument):
    title = db.StringField(max_length=50, required=True)
    link = db.StringField(max_length=255, required=True)
    icon = db.StringField(max_length=255)
    css_class = db.StringField(max_length=50)
    order = db.IntField(default=0)

    def __unicode__(self):
        return '{0} -> {1}'.format(self.title, self.link)


class User(db.DynamicDocument, UserMixin):
    name = db.StringField(max_length=255)
    email = db.EmailField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(
        db.ReferenceField(Role, reverse_delete_rule=db.DENY), default=[]
    )

    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField(max_length=255)
    current_login_ip = db.StringField(max_length=255)
    login_count = db.IntField()

    username = db.StringField(max_length=50, requied=False, unique=True)

    @classmethod
    def generate_username(cls, name, user=None):
        name = name or ''
        username = slugify(name)
        filters = dict(username=username)
        if user:
            filters['id__ne'] = user.id
        if cls.objects.filter(**filters).count():
            username = '{0}{1}'.format(username, random.randint(1, 1000))
        return username

    def set_password(self, password, save=False):
        self.password = encrypt_password(password)
        if save:
            self.save()

    @classmethod
    def create_user(cls, name, email, password, active=True, roles=None,
                    username=None, *args, **kwargs):

        username = username or cls.generate_username(name)

        if 'links' in kwargs:
            kwargs['links'] = [UserLink(**link) for link in kwargs['links']]

        return cls.objects.create(
            name=name,
            email=email,
            password=encrypt_password(password),
            active=active,
            roles=roles,
            username=username,
            *args,
            **kwargs
        )

    @property
    def connections(self):
        return Connection.objects(user_id=str(self.id))

    def __unicode__(self):
        return '{0} <{1}>'.format(self.name or '', self.email)


class Connection(db.Document):
    user_id = db.ObjectIdField()
    provider_id = db.StringField(max_length=255)
    provider_user_id = db.StringField(max_length=255)
    access_token = db.StringField(max_length=255)
    secret = db.StringField(max_length=255)
    display_name = db.StringField(max_length=255)
    full_name = db.StringField(max_length=255)
    profile_url = db.StringField(max_length=512)
    image_url = db.StringField(max_length=512)
    rank = db.IntField(default=1)

    @property
    def user(self):
        return User.objects(id=self.user_id).first()
