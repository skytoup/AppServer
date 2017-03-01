# -*- coding: utf-8 -*-
# Created by apple on 2017/2/7.

from ..config import Config
from sanic import Blueprint

static_blueprint = Blueprint('static', Config.static_main)

# 静态文件
static_blueprint.static(Config.static_icon, Config.icon_dir)
static_blueprint.static(Config.static_app, Config.app_dir)
static_blueprint.static(Config.static_cer, Config.ca_file)
