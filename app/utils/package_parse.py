# -*- coding: utf-8 -*-
# Created by apple on 2017/1/31.

import re
import aiofiles
import plistlib
from platform import system
from .regex import Regex
from ..log import log
from zipfile import ZipFile
from subprocess import Popen, PIPE
from ..db import AppType

aapt = './aapt_mac' if system() == 'Darwin' else './aapt_centos'


class PackageParse:
    __apk_manifest_path = 'AndroidManifest.xml'

    @classmethod
    async def parse(cls, package_path: str):
        """
        解析安装包(ipa、apk)
        :param package_path: 安装包路径
        :return: 成功解析返回 PackageParse, 失败返回 None
        """
        if package_path.endswith('.ipa'):
            return await cls.__ipa_parse(package_path)
        elif package_path.endswith('.apk'):
            return await cls.__apk_parse(package_path)
        else:
            return None

    @staticmethod
    async def __apk_info(file_path: str) -> str:
        """
        获取apk信息
        :param file_path: apk路径
        :return: string
        """
        popen = Popen('{} dump badging {}'.format(aapt, file_path), stdout=PIPE, shell=True)
        result = popen.communicate()[0]
        return result.decode()

    @classmethod
    async def __apk_parse(cls, file_path: str):
        """
        解析apk包
        :param file_path: apk路径
        :return: PackageParse
        """
        apk_file = ZipFile(file_path)
        info = await cls.__apk_info(file_path)

        match_info = Regex.APKInfo.match(info)
        package_name = match_info.group(1)
        version_name = match_info.group(3)
        version_code = match_info.group(2)

        names = Regex.APKName.findall(info)
        app_name = names[0] if names else package_name
        icon_path = Regex.APKIcon.findall(info)[0]

        log.debug('app: {}, V{} build {}, package: {}'.format(app_name, version_name, version_code, package_name))
        return PackageParse(apk_file, AppType.android, package_name, app_name, icon_path, version_name, version_code)

    @staticmethod
    async def __ipa_parse(file_path: str):
        """
        解析ipa包
        :param file_path: ipa路径
        :return: PackageParse
        """
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

        # 解析icon'CFBundleIconFiles' (4400546488)
        if plist_file.get('CFBundleIconFiles'):
            icon_name = plist_file['CFBundleIconFiles'][-1]
        else:
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
        re_icon_name_end = '(@\dx)\.png' if not icon_name.endswith('.png') else ''
        re_icon_name = re.compile('([^/]+/){{2}}{}{}'.format(icon_name, re_icon_name_end))
        ns = [n for n in ipa_file.namelist() if re_icon_name.match(n)]
        if not ns:
            log.warning('read icon failure: {}'.format(file_path))
            return
        icon_path = ns[-1]
        log.debug('parse icon path: {}'.format(icon_path))

        # 版本号
        version_number = plist_file['CFBundleShortVersionString']
        # build号
        build_number = plist_file['CFBundleVersion']
        # 包名
        package_name = plist_file['CFBundleIdentifier']
        # app名称
        app_name = plist_file['CFBundleDisplayName'] if plist_file.get('CFBundleDisplayName') else plist_file[
            'CFBundleName']
        log.debug(
            'app: {}, V{} build {}, package: {}'.format(app_name, version_number, build_number, package_name))
        return PackageParse(ipa_file, AppType.iOS, package_name, app_name, icon_path, version_number, build_number)

    def __init__(self, zip_file: ZipFile, app_type: AppType, package_name: str, app_name: str, icon_path: str,
                 version_name: str,
                 version_code: str):
        """
        安装包信息
        :param zip_file: zip_file
        :param app_type: 安装包类型 iOS Android
        :param package_name: 包名
        :param app_name: 应用名
        :param icon_path: logo路径
        :param version_name: 版本名
        :param version_code: 版本号
        """
        self.zip_file = zip_file
        self.app_type = app_type
        self.package_name = package_name
        self.app_name = app_name
        self.icon_path = icon_path
        self.version_name = version_name
        self.version_code = version_code

    async def save_icon(self, save_path):
        async with aiofiles.open(save_path, 'wb+') as f:
            await f.write(self.zip_file.read(self.icon_path))
            if self.app_type == AppType.iOS:
                dirs = save_path.split('/')
                if len(dirs) > 2:
                    save_dir = '/'.join(dirs[:-1])
                else:
                    save_dir = './'
                popen = Popen('./pngdefry -o {} {}'.format(save_dir, save_path), stdout=PIPE, shell=True)
                popen.wait()
