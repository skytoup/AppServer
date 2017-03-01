# -*- coding: utf-8 -*-
# Created by apple on 2017/2/4.

from ..config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库引擎
__engine = create_engine(Config.db_url, echo=Config.debug, logging_name=Config.log_name)

# 配置数据库
Base = declarative_base()

# __metadata = __Base.metadata

# 配置表
from .models import *

# 配置数据库连接
Session = sessionmaker(__engine)


def init():
    # 创建表
    Base.metadata.create_all(__engine)
