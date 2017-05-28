# -*- coding: utf-8 -*-
# Created by apple on 2017/2/5.

import os
from ..log import log
from ..config import Config
from sanic import Blueprint
from sanic.response import text
from sanic.request import Request
from sanic.views import HTTPMethodView
from ..exceptions import BadRequest
from ..utils import JsonResult, Regex, IPAPlist, Date, DB
from ..db import Session, AppModel, AppVersionModel, AppType
from sqlalchemy import desc

app_versions_blueprint = Blueprint('app_version', 'apps/<app_id:int>/versions')


@app_versions_blueprint.route('/page/<page:int>', ['GET'])
async def get_app_versions(request: Request, app_id: int, page: int):
    """
    获取app的版本
    - uri[app_id: int, 页码(从1起)-page: int], format[时间-t: int]
    :param request:
    :param app_id:
    :param page:
    :return:
    """
    time = Date.time2datetime(request.args.get('t'))
    if not time:
        raise BadRequest('')

    if page <= 0:
        log.debug('page need greater zero')
        raise BadRequest('')

    session = Session()
    if not DB.model_exists(session, AppModel, id=app_id):
        raise BadRequest('not find app id: {}'.format(app_id))

    result = session.query(AppVersionModel) \
        .filter(AppVersionModel.app_id == app_id, AppVersionModel.create_at <= time) \
        .order_by(desc(AppVersionModel.create_at)) \
        .offset((page - 1) * Config.app_versions_limit) \
        .limit(Config.app_versions_limit) \
        .all()

    return JsonResult.ok(result).response_json()


class AppVersionView(HTTPMethodView):
    @staticmethod
    async def options(request: Request, app_id: int, package_id: str):
        return text('', headers={
            'Access-Control-Allow-Methods': 'DELETE,OPTIONS',
            'Access-Control-Max-Age:': '62400',
        })

    @staticmethod
    async def delete(request: Request, app_id: int, package_id: str):
        """
        删除app的某个版本
        - uri[app_id: int, package_id: str]
        :param request:
        :param app_id:
        :param package_id:
        :return:
        """
        # if not Regex.APPVersionID.match(package_id):
        #     log.debug('not match version id: {}'.format(package_id))
        #     raise BadRequest('')

        session = Session()
        # 检查是否存在该app
        app_query = DB.model_exists(session, AppModel, id=app_id)
        if not app_query:
            raise BadRequest('not find app id: {}'.format(app_id))

        # 检查app是否存在该版本
        query = DB.model_exists(session, AppVersionModel, app_id=app_id, id=package_id)
        if not query:
            raise BadRequest('not find version id: {} by app id: {}'.format(package_id, app_id))

        # 删除安装包
        model = query.one()
        os.remove(model.package_)

        # 是否所有版本都已经删除
        less_query = DB.model_exists(session, AppVersionModel, app_id=app_id)
        if less_query and less_query.count() == 1:
            os.remove(app_query.one().icon_)
            app_query.delete()

        # 删除版本
        query.delete()
        session.commit()

        log.info('did delete app version: {} by app id: {}'.format(package_id, app_id))
        return JsonResult.ok().response_json()


app_versions_blueprint.add_route(AppVersionView.as_view(), '/<package_id:string>')


@app_versions_blueprint.route('/<package_id:string>/plist')
def get_plist(request: Request, app_id: int, package_id: str):
    """
    获取iPhone在线安装ipa需要的plist
    :param request:
    :param app_id: app的id
    :param package_id: 安装包的id
    :return:
    """
    session = Session()
    # 检查是否存在该app
    app_query = DB.model_exists(session, AppModel, id=app_id, type=AppType.iOS)
    if not app_query:
        raise BadRequest('not find app id: {}'.format(app_id))

    # 检查app是否存在该版本
    app_version_query = DB.model_exists(session, AppVersionModel, app_id=app_id, id=package_id)
    if not app_version_query:
        raise BadRequest('not find version id: {} by app id: {}'.format(package_id, app_id))

    app = app_query.one()
    app_version = app_version_query.one()
    return text(IPAPlist.parse(app_version.package, app.package_name, app_version.version_name, app.name))
