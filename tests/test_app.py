# -*- coding: utf-8 -*-
# Created by apple on 2017/3/13.


import ujson
from .tests import upload, get_apps, get_app_detail, put_app_detail, get_app_versions, del_app_version, del_app


def test_app():
    # 上传
    upload()

    # 获取上传的app
    response = get_apps('all', 1)
    app_json = ujson.loads(response.text)
    apps = app_json.get('datas')
    assert len(apps) != 0
    app = apps[0]
    app_id = app.get('id')
    assert app_id is not None

    # 修改app信息
    name = 'name_1'
    short_chain = 'xxxxxok'
    detail = 'hahaha'
    put_app_detail(app_id, 'name_1', 'xxxxxok', 'hahaha')
    app_detail = get_app_detail(app_id)
    app_detail_json = ujson.loads(app_detail.text)

    # 获取app详情
    app_detail_data = app_detail_json.get('datas')
    assert app_detail_data.get('name') == name
    assert app_detail_data.get('short_chain') == short_chain
    assert app_detail_data.get('detail') == detail

    # 获取app版本
    response = get_app_versions(app_id, 1)
    app_versions_json = ujson.loads(response.text)
    app_versions_data = app_versions_json.get('datas')
    assert len(app_versions_data) != 0
    app_version = app_versions_data[0]
    version_id = app_version.get('id')

    # 删除app版本
    del_app_version(app_id, version_id)

    # 删除app
    del_app(app_id)
