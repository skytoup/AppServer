# -*- coding: utf-8 -*-
# Created by apple on 2017/1/30.

from ..log import log
from .regex import Regex
from zipfile import ZipFile
from ..config import Config
from subprocess import Popen, PIPE

__manifest_path = 'AndroidManifest.xml'


async def __apk_info(file_path):
    popen = Popen('./aapt dump badging {}'.format(file_path), stdout=PIPE, shell=True)
    result = popen.communicate()[0]
    return result.decode()


async def parse(file_path, icon_save_name):
    apk_file = ZipFile(file_path)
    info = await __apk_info(file_path)

    match_info = Regex.APKInfo.match(info)
    package_name = match_info.group(1)
    version_name = match_info.group(3)
    version_code = match_info.group(2)

    match_name_icon = Regex.APKName_Icon.findall(info)[0]
    app_name = match_name_icon[0]
    icon_path = match_name_icon[1]

    icon_save_path = '{}/{}.png'.format(Config.icon_dir, icon_save_name)
    with open(icon_save_path, 'wb+') as f:
        f.write(apk_file.read(icon_path))
        log.debug('save icon success: {}'.format(icon_save_path))

    log.debug('app: {}, V{} build {}, package: {}'.format(app_name, version_name, version_code, package_name))
