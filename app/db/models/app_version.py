# -*- coding: utf-8 -*-
# Created by apple on 2017/1/31.

from .. import Base
from ...config import Config
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.hybrid import hybrid_property


class AppVersionModel(Base):
    __tablename__ = 'app_versions'

    id = Column(String, primary_key=True)
    version_name = Column(String)  # 版本名
    version_code = Column(String)  # 版本号
    update_msg = Column(String)  # 更新说明
    size = Column(String)  # 安装包大小
    package_ = Column(String)  # 安装包路径
    package_uri_ = Column(String)  # 安装包url路径
    create_at = Column(DateTime(True), default=datetime.utcnow)  # 创建时间
    app_id = Column(Integer, ForeignKey('apps.id'), index=True)  # app的id

    __table_args__ = (
        # 联合索引
        UniqueConstraint('id', 'app_id', name='id_app_id'),
        Index('id_app_id', 'id', 'app_id'),
    )

    @hybrid_property
    def package(self):
        return '{}{}{}'.format(Config.url, Config.static_main, self.package_uri_)

    @hybrid_property
    def plist(self):
        return '{}/apps/{}/versions/{}/plist'.format(Config.url, self.app_id, self.id) if self.package_.endswith(
            '.ipa') else None
