# -*- coding: utf-8 -*-
# Created by apple on 2017/2/4.

import enum
from .. import Base
from ...config import Config
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Enum, Index, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property


class AppType(enum.Enum):
    iOS = 0
    android = 1


class AppModel(Base):
    __tablename__ = 'apps'

    id = Column(Integer, primary_key=True, autoincrement=True)  # sqlite_autoincrement
    type = Column(Enum(AppType))  # iOS: 0, Android: 1
    short_chain_uri_ = Column(String, unique=True)  # 短链
    detail = Column(String)  # 描述
    name = Column(String)  # 名称
    package_name = Column(String)  # 包名
    icon_ = Column(String)  # icon路径
    icon_uri_ = Column(String)  # icon url 路径
    create_at = Column(DateTime(True), default=datetime.now)  # 创建时间(本地时间)
    versions_relationship = relationship('AppVersionModel'),  # app的版本

    __table_args__ = (
        # 联合索引
        UniqueConstraint('type', 'package_name', name='uix_type_package_name'),
        Index('uix_type_package_name', 'type', 'package_name'),
    )

    @hybrid_property
    def icon(self):
        return '{}{}{}'.format(Config.url, Config.static_main, self.icon_uri_)

    @hybrid_property
    def short_chain(self):
        return self.short_chain_uri_
