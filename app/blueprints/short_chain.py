# -*- coding: utf-8 -*-
# Created by apple on 2017/2/23.

from ..utils import DB
from ..config import Config
from sanic import Blueprint
from sanic.request import Request
from ..db import AppModel, Session
from sanic.response import html
from ..exceptions import BadRequest

short_chain_blueprint = Blueprint('short_chain', '/')


@short_chain_blueprint.route('<short_chain:[a-zA-Z0-9]\w{4,14}>')
def short_chain(request: Request, short_chain: str):
    """
    短链接进入App详情
    :param request:
    :param short_chain: 短链接
    :return:
    """
    session = Session()
    query = DB.model_exists(session, AppModel, short_chain_uri_=short_chain)
    if not query:
        raise BadRequest('not find short chain: {}'.format(short_chain))
    model = query.one()
    url = '{}/#/app/{}'.format(Config.url, model.id)
    # return redirect('/#/app/{}'.format(model.id))
    return html('''
<html>
    <header>
    </header>

    <body style="padding: 30px">
        <div>跳转中...</div>
        <a href='{0}'>如果没有打开请点击这里</a>
    </body>

    <script>
        setTimeout("location.href='{0}'", 2000);
    </script>
</html>
    '''.format(url))
