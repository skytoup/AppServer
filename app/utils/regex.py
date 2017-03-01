# -*- coding: utf-8 -*-
# Created by apple on 2017/2/7.

import re


class Regex:
    IPAInfoPlistPath = re.compile('([^/]+/){2}Info\.plist')  # 匹配`info.plist`路径
    APKInfo = re.compile("package: name='(.+?)' versionCode='(.+?)' versionName='(.+?)'")  # 匹配aapt获取的apk信息
    APKName = re.compile("label='([^']+?)'")  # 匹配aapt获取的apk name 和 icon
    APKIcon = re.compile("icon='([^']+?)'")  # 匹配aapt获取的apk name 和 icon

    ShortChina = re.compile('^[a-zA-Z0-9]\w{4,14}$')  # 匹配短链, 字母开头, 5-15位字母、数字、下划线
    APPVersionID = re.compile('^[a-zA-Z0-9]{16}$')  # 匹配app version的id, 16位字母、数字
