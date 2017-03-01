# -*- coding: utf-8 -*-
# Created by apple on 2017/1/30.

import os
import logging
from subprocess import Popen


class BaseConfig:
    # server config
    host = '10.0.1.90'  # 服务器访问地址
    bing = '0.0.0.0'  # 绑定地址
    port = 8000  # 绑定端口
    debug = False  # 是否为测试模式
    url = None

    # static 静态uri
    static_main = '/static'
    static_icon = '/icon'
    static_app = '/app'
    static_plist = '/plist'
    static_cer = '/cer/ca.cer'
    static_html = '/'

    # limit, 分页
    apps_limit = 8  # 每页app数
    app_versions_limit = 8  # 每页app version数

    # dir or file path 静态文件夹、文件
    data_dir = 'data'
    app_dir = '{}/app'.format(data_dir)
    log_dir = 'log'
    icon_dir = '{}/icon'.format(data_dir)
    cer_dir = '{}/cer'.format(data_dir)
    db_dir = '{}/db'.format(data_dir)
    plist_dir = '{}/plist'.format(data_dir)
    html_dir = 'html'
    log_file = '{}/app.log'.format(log_dir)
    generate_certificate_file = './generate_certificate.sh'
    ca_file = '{}/ca.cer'.format(cer_dir)
    host_file = '{}/host'.format(cer_dir)
    server_key_file = '{}/server.key'.format(cer_dir)
    server_cer_file = '{}/server.cer'.format(cer_dir)

    # log config
    log_name = 'AppServer'
    log_level = logging.WARNING
    log_file_max_byte = 1024 * 1024 * 100  # 100M
    log_file_backup_count = 10

    # db
    db_name = 'app_server.db'
    db_url = 'sqlite:///{}/{}'.format(db_dir, db_name)


class DebugConfig(BaseConfig):
    """
    Debug的配置
    """
    debug = True
    log_level = logging.DEBUG


class ProductionConfig(BaseConfig):
    """
    Product的配置
    """
    pass


Config = DebugConfig
Config.url = 'https://{}:{}'.format(Config.host, Config.port)

# 创建需要的目录
paths = [Config.data_dir, Config.app_dir, Config.log_dir, Config.icon_dir, Config.db_dir, Config.plist_dir]
not_exists_dirs = [path for path in paths if not os.path.isdir(path)]
for directory in not_exists_dirs:
    os.mkdir(directory)

# 创建自签证书
pre_host = None
if os.path.isfile(Config.host_file):
    with open(Config.host_file) as hf:
        pre_host = hf.read()

if pre_host != Config.host or not os.path.isfile(Config.ca_file):
    Popen('{} {} {}'.format(Config.generate_certificate_file, Config.host, Config.cer_dir), shell=True).wait()
    with open(Config.host_file, 'wb+') as f:
        f.write(Config.host.encode())
