# -*- coding: utf-8 -*-
# Created by apple on 2017/2/28.


class Byte:
    @staticmethod
    def pretty(byte: int) -> str:
        """
        更好地显示byte
        :param byte: byte
        :return: 格式化的byte
        """
        file_size = None
        if byte >= 1073741824:  # g
            file_size = '{:.2f}G'.format(byte / 1073741824)
        elif byte >= 1048576:  # m
            file_size = '{:.2f}M'.format(byte / 1048576)
        elif byte >= 1024:  # k
            file_size = '{:.2f}K'.format(byte / 1024)
        elif byte < 1024:  # b
            file_size = '{}b'.format(byte)
        return file_size
