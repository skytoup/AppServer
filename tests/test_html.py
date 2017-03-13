# -*- coding: utf-8 -*-
# Created by apple on 2017/3/13.


from app import app


def test_index():
    _, response = app.test_client.get('/')
    assert response.status == 200
    assert len(response.history) != 0
    assert response.url.endswith('index.html')


# FIXME: - test_client获取binary时, 会错误
# def test_icon():
#     _, response = app.test_client.get('/favicon.ico')
#     assert response.status == 200
