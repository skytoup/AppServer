# -*- coding: utf-8 -*-
# Created by apple on 2017/2/5.

import datetime
import enum
from sqlalchemy.ext.declarative import DeclarativeMeta


# 序列化 SqlAlchemy 的结果为 json 字符串 https://my.oschina.net/gongshang/blog/395431?p=1
class AlchemyEncoder:
    @staticmethod
    def decode(obj):
        if obj and isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and not x.endswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if isinstance(data, datetime.datetime):
                    fields[field] = data.timestamp()
                elif isinstance(data, datetime.date):
                    fields[field] = data.isoformat()
                elif isinstance(data, datetime.timedelta):
                    fields[field] = (datetime.datetime.min + data).time().isoformat()
                elif isinstance(data, int) or isinstance(data, float) or isinstance(data, str):
                    fields[field] = data
                elif isinstance(data, enum.Enum):
                    fields[field] = data.value
                elif isinstance(data.__class__, DeclarativeMeta):
                    fields[field] = AlchemyEncoder.decode(data)
                elif isinstance(data, list):
                    fields[field] = [AlchemyEncoder.decode(d) for d in data]
            return fields
        else:
            return obj
