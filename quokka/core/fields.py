# -*- coding: utf-8 -*-
# -*- date: 2016-02-25 23:51 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from mongoengine import fields
from mongoengine.base import BaseList


class MultipleObjectsReturned(Exception):
    pass


def match_all(i, kwargs):
    return all(getattr(i, k) == v for k, v in kwargs.items())


def only_matches(obj, kwargs, silent=True):
    if kwargs and silent:
        return obj
    return filter(lambda i: match_all(i, kwargs), obj)


def get_instance(_instance):
    return _instance.__class__.objects.get(pk=_instance.pk)


def update_item(item, new_values):
    if not isinstance(new_values, dict):
        return
    for k, v in new_values.items():
        setattr(item, k, v)


def _filter(self):
    def inner(*args, **kwargs):
        values = only_matches(self, kwargs)
        return FilteredList(values, get_instance(self._instance), self._name)

    return inner


def _exclude(self):
    def inner(*args, **kwargs):
        _values = only_matches(self, kwargs, silent=False)
        values = [item for item in self if item not in _values]
        return FilteredList(values, get_instance(self._instance), self._name)

    return inner


def _create(self):
    def inner(*args, **kwargs):
        instance = self._instance
        item_cls = instance._fields[self._name].field.document_type_obj
        item = item_cls(**kwargs)
        self.append(item)
        instance.save()
        return item

    return inner


def _get(self):
    def inner(*args, **kwargs):
        values = only_matches(self, kwargs)
        values = list(values)
        if len(values) > 1:
            raise MultipleObjectsReturned('More than one object returned')
        return values and values[0]

    return inner


def _update(self):
    def inner(new_values, **kwargs):
        values = only_matches(self, kwargs)
        for item in values:
            update_item(item, new_values)
        self._instance.save()
        self._instance.reload()
        if len(values) > 1:
            return FilteredList(
                values,
                get_instance(self._instance),
                self._name
            )
        else:
            return values and values[0]

    return inner


def _delete(self):
    def inner(*args, **kwargs):
        values = only_matches(self, kwargs)
        for item in values:
            self.remove(item)
        self._instance.save()
        self._instance.reload()
        if len(values) > 1:
            return FilteredList(
                values,
                get_instance(self._instance),
                self._name
            )
        else:
            return values and values[0]

    return inner


def _count(self):
    def inner(*args, **kwargs):
        return len(self)

    return inner


def inject(obj):
    setattr(obj, 'filter', _filter(obj))
    setattr(obj, 'exclude', _exclude(obj))
    setattr(obj, 'create', _create(obj))
    setattr(obj, 'get', _get(obj))
    setattr(obj, 'update', _update(obj))
    setattr(obj, 'delete', _delete(obj))
    setattr(obj, 'count', _count(obj))


class FilteredList(BaseList):
    def __init__(self, *args, **kwargs):
        super(FilteredList, self).__init__(*args, **kwargs)
        inject(self)


class ListField(fields.ListField):
    # validators = list()
    # filters = list()

    def __get__(self, *args, **kwargs):
        value = super(ListField, self).__get__(*args, **kwargs)
        inject(value)
        return value
