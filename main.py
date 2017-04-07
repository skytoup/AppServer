# -*- coding: utf-8 -*-
# Created by apple on 2017/1/30.

import ssl
from app import app
from app.config import Config

# https
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=Config.server_cer_file, keyfile=Config.server_key_file)

app.run(Config.bing, Config.port, Config.debug, ssl=context, workers=Config.workers)
