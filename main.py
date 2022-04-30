#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# QGMA主程序 #
# 作者：稽术宅（funnygeeker）
# QGMA项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/qgma

from asyncio.log import logger
import os
import sys
os.chdir(sys.path[0])  # 改变程序当前工作路径

from core.log_mgt import *
Handle_Log.Log_Conf()
logger.debug('1')
import test