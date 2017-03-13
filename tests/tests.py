# -*- coding: utf-8 -*-
# Created by apple on 2017/3/13.


import time
import ujson
from app import app
from aiohttp import FormData


def response_normal_check(response):
    assert response.status == 200
    assert ujson.loads(response.text).get('ok') is True


def get_apps(app_type, page):
    _, response = app.test_client.get('/apps/{}/page/{}?t={}'.format(app_type, page, time.time()))
    response_normal_check(response)
    json = ujson.loads(response.text)
    assert json.get('datas') is not None
    return response


def upload():
    data = FormData()
    data.add_field('package', open('tests/QXmokuai_3.apk', 'rb'), filename='QXmokuai_3.apk')
    data.add_field('msg', 'test upload')
    _, response = app.test_client.post('/upload/app', data=data)
    response_normal_check(response)
    return response


def get_app_detail(app_id):
    _, response = app.test_client.get('/apps/{}'.format(app_id))
    response_normal_check(response)
    return response


def get_app_versions(app_id, page):
    _, response = app.test_client.get('/apps/{}/versions/page/{}?t={}'.format(app_id, page, time.time()))
    response_normal_check(response)
    return response


def put_app_detail(app_id, name, short_chain, detail):
    _, response = app.test_client.put('/apps/{}'.format(app_id),
                                      data=ujson.dumps(dict(name=name, short_chain=short_chain, detail=detail)))
    response_normal_check(response)
    return response


def del_app(app_id):
    _, response = app.test_client.delete('/apps/{}'.format(app_id))
    response_normal_check(response)
    return response


def del_app_version(app_id, package_id):
    _, response = app.test_client.delete('/apps/{}/versions/{}'.format(app_id, package_id))
    response_normal_check(response)
    return response
