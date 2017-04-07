# -*- coding: utf-8 -*-
# Created by apple on 2017/4/7.

import os
from .config import Config
from subprocess import Popen

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
