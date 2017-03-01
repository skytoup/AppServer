# -*- coding: utf-8 -*-
# Created by apple on 2017/2/5.

from .alchemy_json_encoder import AlchemyEncoder
from sanic.response import json


class JsonResult:
    @classmethod
    def ok(cls, datas=None):
        return JsonResult(True, 0, '', cls.__encode_datas(datas))

    @classmethod
    def not_ok(cls, msg, code=-1, datas=None):
        return JsonResult(False, code, msg, cls.__encode_datas(datas))

    @staticmethod
    def __encode_datas(datas):
        if isinstance(datas, list):
            return [AlchemyEncoder.decode(data) for data in datas]
        else:
            return AlchemyEncoder.decode(datas)

    def __init__(self, ok, code, msg, datas):
        if ok is not None:
            self.ok = ok
        if code is not None:
            self.code = code
        if msg is not None:
            self.msg = msg
        if datas is not None:
            self.datas = datas

    def response_json(self, **kwargs):
        return json(self, **kwargs)
