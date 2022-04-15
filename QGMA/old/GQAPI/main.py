#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import os,sys
    os.chdir(sys.path[0]) # 改变程序当前工作路径
    from src.log import *
    from src.settings import *
    try:
        Set_Log(log_file_name=settings['debug']['log_file_name'], file_log_level=settings['debug']['file_log_level'], console_log_level=settings['debug']['console_log_level']) # 初始化日志模块
    except KeyError:
        print('error')

    except:
        Set_Log()
        logger.critical('日志设置加载错误,其他错误：\n'+Get_Error())
        quit()

    logger.debug('ok')