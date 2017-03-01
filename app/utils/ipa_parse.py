# -*- coding: utf-8 -*-
# Created by apple on 2017/1/30.

import re
import plistlib
from ..log import log
from .regex import Regex
from zipfile import ZipFile
from ..config import Config


async def parse(file_path, icon_save_name):
    ipa_file = ZipFile(file_path)

    # 解析info.plist路径
    ns = [n for n in ipa_file.namelist() if Regex.IPAInfoPlistPath.match(n)]
    if not ns:
        log.warning('parse info.plist failure: {}'.format(file_path))
        return
    plist_path = ns[-1]

    # 解析plist
    plist_data = ipa_file.read(plist_path)
    plist_file = plistlib.loads(plist_data)

    # 解析icon
    if plist_file.get('CFBundleIcons'):
        icon_dict = plist_file['CFBundleIcons']
    elif plist_file.get('CFBundleIcons'):
        icon_dict = plist_file['CFBundleIcons~ipad']
    else:
        log.warning('parse icon failure: {}'.format(file_path))
        return
    icon_name = icon_dict['CFBundlePrimaryIcon']['CFBundleIconFiles'][-1]
    log.debug('parse icon name: {}'.format(icon_name))

    # 获取icon路径
    ns = [n for n in ipa_file.namelist() if re.match('([^/]+/){{2}}{}(@\dx)\.png'.format(icon_name), n)]
    if not ns:
        log.warning('read icon failure: {}'.format(file_path))
        return
    icon_path = ns[-1]
    log.debug('parse icon path: {}'.format(icon_path))

    icon_save_path = '{}/{}.png'.format(Config.icon_dir, icon_save_name)
    with open(icon_save_path, 'wb+') as f:
        f.write(ipa_file.read(icon_path))
        log.debug('save icon success: {}'.format(icon_save_path))

    # 版本号
    version_number = plist_file['CFBundleShortVersionString']
    # build号
    build_number = plist_file['CFBundleVersion']
    # 包名
    package_name = plist_file['CFBundleIdentifier']
    # app名称
    app_name = plist_file['CFBundleDisplayName'] if plist_file.get('CFBundleDisplayName') else plist_file[
        'CFBundleName']
    log.debug('app: {}, V{} build {}, package: {}'.format(app_name, version_number, build_number, package_name))

    # PackageInfoModel()
