#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# QGMA配置文件管理模块
# 作者：稽术宅（funnygeeker）
# QGMA项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/qgma
# 参考资料：
# chardet文本编码检测：https://blog.csdn.net/tianzhu123/article/details/8187470

from configobj import ConfigObj
from text_mgt import *


class Conf_Mgt:
    '存储设置变量及设置操作函数'
    connect_config = {}
    debug_config = {}

    def Conf_Read(file_path, encoding=''):
        '读取设置文件 返回：dict'
        if encoding == '':  # 如果没有设置读取文件的编码
            encoding = Text_Mgt.Encodeing_Detect(file_path=file_path)
        return ConfigObj(file_path, encoding=encoding)


if __name__ == '__main__':
    print(Conf_Mgt.Conf_Read('./tests/text/settings.ini'))
