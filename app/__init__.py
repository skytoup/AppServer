# -*- coding: utf-8 -*-
# Created by apple on 2017/1/30.

from app import db
from sanic import Sanic
from sanic.request import Request
from sanic.response import redirect
from .config import Config
from .blueprints import *

db.init()

app = Sanic(__name__)

# blueprints
app.blueprint(static_blueprint)
app.blueprint(upload_blueprint)
app.blueprint(apps_blueprint)
app.blueprint(app_versions_blueprint)
app.blueprint(exception_blueprint)
app.blueprint(short_chain_blueprint)
app.static(Config.static_html, Config.html_dir)


@app.route('/')
async def index(request: Request):
    return redirect('/index.html')

# 允许跨域
# @app.middleware('response')
# async def access_control_all_origin(request: Request, response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
