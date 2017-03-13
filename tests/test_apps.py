# -*- coding: utf-8 -*-
# Created by apple on 2017/3/13.

from .tests import get_apps


def test_get_apps():
    types = [
        'iOS',
        'all',
        'android'
    ]
    for t in types:
        get_apps(t, 1)
