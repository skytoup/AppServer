# -*- coding: utf-8 -*-
# Created by apple on 2017/2/21.

from datetime import datetime
from ..log import log


class Date:
    @staticmethod
    def time2datetime(t) -> datetime:
        """
        时间戳转datetime
        :param t: 1970开始的秒数
        :return:
        """
        if t:
            try:
                return datetime.fromtimestamp(float(t))
            except ValueError:
                log.debug('t is not a number')
        else:
            log.debug('not format param t')
