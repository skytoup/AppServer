# -*- coding: utf-8 -*-
# Created by apple on 2017/2/6.

from sanic.exceptions import SanicException


class BadRequest(SanicException):
    status_code = 200
