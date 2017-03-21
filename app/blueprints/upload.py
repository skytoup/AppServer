# -*- coding: utf-8 -*-
# Created by apple on 2017/1/30.

import os
import time
import aiofiles
from ..log import log
from sanic import Blueprint
from ..config import Config
from sanic.response import text
from sanic.request import Request
from ..exceptions import BadRequest
from shortuuid import uuid, random
from sanic.views import HTTPMethodView
from ..utils import PackageParse, JsonResult, Byte
from ..db import Session, AppModel, AppVersionModel

upload_blueprint = Blueprint('upload', 'upload')


class UploadApp(HTTPMethodView):
    @staticmethod
    async def options(request: Request):
        return text('', headers={
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Headers': 'X-Requested-With',
            'Access-Control-Max-Age:': '62400',
        })

    @staticmethod
    async def post(request: Request):
        """
        上传app, format[安装包-package: file, 更新说明(默认为空)-msg: str]
        :param request:
        :return:
        """
        file = request.files.get('package')
        update_msg = request.form.get('msg') or ''
        if not file:
            log.warning('not upload file')
            raise BadRequest('not find file')

        session = Session()
        while 1:
            # 安装包id
            fid = uuid('{}-{}'.format(id(Request), time.time()), 16)
            if not session.query(AppVersionModel).filter_by(id=fid).count():
                break
        file_name = '{}.{}'.format(fid, file.name[file.name.rfind('.') + 1:])
        file_path = '{}/{}'.format(Config.app_dir, file_name)

        # 保存安装包
        async with aiofiles.open(file_path, 'wb+') as f:
            await f.write(file.body)
            log.debug('save upload success: {}'.format(file_path))

        package = await PackageParse.parse(file_path)
        if not package:
            os.remove(file_path)
            raise BadRequest('the file is not support')

        app_query = session.query(AppModel).filter_by(package_name=package.package_name, type=package.app_type)

        if app_query.count():  # 已存在
            exists = True
            app = app_query.one()
        else:  # 不存在
            exists = False
            # 生成短链
            while 1:
                short_chain = random(8)
                if not session.query(AppModel).filter_by(short_chain_uri_=short_chain).count():
                    break

            app_uuid = uuid('+_{}-{}_+'.format(package.app_type, package.package_name), 16)
            icon_name = '{}.{}'.format(app_uuid, package.icon_path[package.icon_path.rfind('.') + 1:])
            app = AppModel(type=package.app_type, short_chain_uri_=short_chain, detail='', name=package.app_name,
                           package_name=package.package_name, icon_='{}/{}'.format(Config.icon_dir, icon_name),
                           icon_uri_='{}/{}'.format(Config.static_icon, icon_name))
            session.add(app)
            session.commit()
            app.version_code = package.version_code
            app.version_name = package.version_name

        # 保存图标
        await package.save_icon(app.icon_)

        file_byte = os.path.getsize(file_path)
        file_size = Byte.pretty(file_byte)

        app_version = AppVersionModel(id=fid, version_name=package.version_name, version_code=package.version_code,
                                      update_msg=update_msg,
                                      size=file_size, package_='{}/{}'.format(Config.app_dir, file_name),
                                      package_uri_='{}/{}'.format(Config.static_app, file_name),
                                      app_id=app.id)
        session.add(app_version)
        session.commit()

        # app不存在时, 返回app信息
        return JsonResult.ok(app if not exists else None).response_json()


upload_blueprint.add_route(UploadApp.as_view(), '/app')
