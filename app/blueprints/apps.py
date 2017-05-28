# -*- coding: utf-8 -*-
# Created by apple on 2017/2/5.

import os
from ..log import log
from ..config import Config
from sqlalchemy import func, desc
from sanic import Blueprint
from sanic.request import Request
from sanic.response import text
from ..exceptions import BadRequest
from ..utils import JsonResult, Regex, Date, DB
from sanic.views import HTTPMethodView
from ..db import Session, AppModel, AppVersionModel

apps_blueprint = Blueprint('apps', 'apps')


@apps_blueprint.route('/<app_type:iOS|android|all>/page/<page:int>', ['GET'])
async def get_apps(request: Request, app_type: str, page: int):
    """
    获取app
    - uri[app类型(all/iOS/android)-app_type: str, 页码(从1起)-page: int], format[时间s-t: int]
    :param request:
    :return:
    """
    time = Date.time2datetime(request.args.get('t'))
    if not time:
        raise BadRequest('')

    if page <= 0:
        log.debug('page need greater zero')
        raise BadRequest('')

    kw = request.args.get('kw')

    session = Session()
    query = session.query(AppModel, AppVersionModel.version_code, AppVersionModel.version_name,
                          func.max(AppVersionModel.create_at).label('_update_at')) \
        .join(AppVersionModel, AppModel.id == AppVersionModel.app_id) \
        .filter(AppModel.create_at <= time)
    if app_type != 'all':  # 安装包类型过滤
        query = query.filter(AppModel.type == app_type)

    if kw:
        query = query.filter(AppModel.name.like('%{}%'.format(kw)))

    result = query.order_by(desc(AppModel.create_at)) \
        .group_by(AppModel.short_chain_uri_) \
        .offset((page - 1) * Config.apps_limit) \
        .limit(Config.apps_limit) \
        .all()

    datas = []
    for app, version_code, version_name, _ in result:
        app.version_code = version_code
        app.version_name = version_name
        datas.append(app)

    return JsonResult.ok(datas).response_json()


class AppsView(HTTPMethodView):
    @staticmethod
    async def options(request: Request, app_id: int):
        return text('', headers={
            'Access-Control-Allow-Methods': 'GET,PUT,DELETE,OPTIONS',
            'Access-Control-Max-Age:': '62400',
        })

    @staticmethod
    async def get(request: Request, app_id: int):
        """
        获取app详情
        - uri[app_id: int]
        :param request:
        :param app_id:
        :return:
        """
        session = Session()
        query = DB.model_exists(session, AppModel, id=app_id)
        if not query:
            raise BadRequest('not find app id: {}'.format(app_id))

        app = query.one()
        return JsonResult.ok(app).response_json()

    @staticmethod
    async def delete(request: Request, app_id: int):
        """
        删除app
        - uri[app_id: int]
        :param request:
        :param app_id:
        :return:
        """
        session = Session()
        app_query = DB.model_exists(session, AppModel, id=app_id)
        if not app_query:
            raise BadRequest('not find app id: {}'.format(app_id))

        # 删除图标
        app = app_query.one()
        os.remove(app.icon_)
        # 删除app的所有版本
        app_version_query = session.query(AppVersionModel).filter(AppVersionModel.app_id == app_id)
        for model in app_version_query.all():
            os.remove(model.package_)
        app_version_query.delete()

        # 删除app
        app_query.delete()
        session.commit()
        log.info('did delete app id: {}'.format(app_id))

        return JsonResult.ok().response_json()

    @staticmethod
    async def put(request: Request, app_id: int):
        """
        修改app信息
        - uri[app_id: int], json(最少包含一个参数)[name: str, short_chain: str, detail: str]
        :param request:
        :param app_id:
        :return:
        """
        json = request.json
        if not isinstance(json, dict):
            log.debug('json it not a dict')
            raise BadRequest('')

        name = json['name'].strip() if isinstance(json.get('name'), str) else None
        short_chain = json['short_chain'].strip() if isinstance(json.get('short_chain'), str) else None
        detail = json['detail'].strip() if isinstance(json.get('detail'), str) else None
        if not (name or short_chain) and detail is None:
            log.debug('need name, short chain or detail, less one')
            raise BadRequest('')

        session = Session()
        query = DB.model_exists(session, AppModel, id=app_id)
        if not query:
            raise BadRequest('not find app id: {}'.format(app_id))

        if short_chain:
            if not Regex.ShortChina.match(short_chain):
                log.debug(
                    'short chain length need 5-15 and combination of letters, Numbers, underline')
                raise BadRequest(
                    'short chain length need greater 5 and letter by the combination of letters, Numbers, underline')
            elif session.query(AppModel).filter(AppModel.short_chain_uri_ == short_chain,
                                                AppModel.id != app_id).count() != 0:
                log.debug('short chain did exists')
                raise BadRequest('short chain did exists')

        app = query.one()
        if name:
            app.name = name
        if short_chain:
            app.short_chain_uri_ = short_chain
        if detail is not None:
            app.detail = detail

        session.commit()
        log.debug('did modify app: {}, {} - {} - {}'.format(app.package_name, name, short_chain, detail))

        return JsonResult.ok().response_json()


apps_blueprint.add_route(AppsView.as_view(), '/<app_id:int>')


# @apps_blueprint.route('/search', ['GET'])
# async def search(request: Request):
#     time = Date.time2datetime(request.args.get('t'))
#     if not time:
#         raise BadRequest('')
#
#     page = request.args.get('page')
#     if page <= 0:
#         log.debug('page need greater zero')
#         raise BadRequest('')
#
#     kw = request.args.get('kw')
#     if not kw:
#         raise BadRequest('')
#
#     app_type = request.args.get('type')
#
#     session = Session()
#     session.query(AppModel).filter(AppModel.create_at <= time, AppModel.type == app_type) \
#         .offset((page - 1) * Config.apps_limit) \
#         .limit(Config.apps_limit) \
#         .all()
#     session.commit()
