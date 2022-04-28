#!/usr/bin/env python
# -*- coding:utf-8 -*-
# https://www.cnblogs.com/xyztank/articles/13599165.html
# https://www.cnblogs.com/pyxiaomangshe/p/7918850.html
# https://blog.csdn.net/qq_36072270/article/details/105345562

import os,sys
import traceback
import logging
import colorlog
from logging.handlers import RotatingFileHandler


cur_path = os.path.dirname(os.path.realpath(__file__))  # 当前项目路径
log_path = os.path.join(os.path.dirname(cur_path),
                        'logs')  # log_path为存放日志的路径
if not os.path.exists(log_path):
    os.mkdir(log_path)  # 若不存在logs文件夹，则自动创建
# 日志设置 #
# 日志文件名
# 文件日志等级
# 控制台日志等级
# 最大单个日志大小
# 最大创建日志数量
class Handle_Log:
    def Log_Conf(log_file_name='gqapi.log', file_log_level='debug', console_log_level='debug', max_bytes=1*1024*1024, backup_count=0):
        log_file_name = str(log_file_name)
        for temp in ['\\', '/', ':', '*', '\"', '<', '>', '|']:
            log_file_name = log_file_name.replace(temp, '')
        for temp in ['', '.', '..']:
            if log_file_name == temp:  # 避免文件名不合法
                log_file_name = 'gqapi.log'
                break

        global logger
        logger = logging.getLogger()

        log_colors_config = {
            # 终端输出日志颜色配置
            'DEBUG': 'bold_cyan',
            'INFO': 'white',
            'WARNING': 'black,bg_yellow',
            'ERROR': 'black,bg_red',
            'CRITICAL': 'black,bg_purple',
        }
        # logger = builtins.logger = logging.getLogger() # 使logger可以全局调用且ide不报错

        # 输出到控制台
        console_handler = logging.StreamHandler()
        # 输出到文件
        file_handler = RotatingFileHandler(filename=(
            log_path+'/'+log_file_name), mode='a', maxBytes=max_bytes, backupCount=backup_count,  encoding='utf8')

        # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
        logger.setLevel(logging.DEBUG)
        log_level = [file_log_level, console_log_level]  # 每项的日志等级
        log_handler = [file_handler, console_handler]  # 每个日志等级对应的对象
        log_tips = ''  # 日志等级配置错误提示
        for temp in range(len(log_level)):
            log_level[temp] = str(log_level[temp])
            if log_level[temp] == '1':
                log_handler[temp].setLevel(logging.DEBUG)
            elif log_level[temp] == '2':
                log_handler[temp].setLevel(logging.INFO)
            elif log_level[temp] == '3':
                log_handler[temp].setLevel(logging.WARNING)
            elif log_level[temp] == '4':
                log_handler[temp].setLevel(logging.ERROR)
            elif log_level[temp] == '5':
                log_handler[temp].setLevel(logging.CRITICAL)
            else:
                log_handler[temp].setLevel(logging.DEBUG)
                log_tips = '日志等级配置错误，将默认使用DEBUG等级！'

        # 日志输出格式
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d]->[%(levelname)s]: \n%(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d]->[%(levelname)s]: \n%(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config
        )
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # 重复日志问题：
        # 1、防止多次addHandler；
        # 2、loggername 保证每次添加的时候不一样；
        # 3、显示完log之后调用removeHandler
        if not logger.handlers:
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

        console_handler.close()
        file_handler.close()

        if log_tips != '':
            logger.error(log_tips)
        logger.debug('日志模块（./src/log.py）配置完毕...')

    def Get_Error(level=''):
        ttype,tvalue,ttraceback = sys.exc_info()
        error_msg = ''
        for temp in traceback.format_tb(ttraceback):
            error_msg += temp
        if 'ERROR' == str.upper(level):
            logger.error(traceback.format_exc())
        else:
            logger.critical(traceback.format_exc())
            quit()

'''
输出format参数中可能用到的格式化串：
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名
%(funcName)s 调用日志输出函数的函数名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s用户输出的消息

**注：1和3/4只设置一个就可以，如果同时设置了1和3，log日志中会出现一条记录存了两遍的问题。
'''

'''
格式化符号
python中时间日期格式化符号：
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12） 
%M 分钟数（00=59）
%S 秒（00-59）

%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身 

'''

if __name__ == '__main__': # 代码测试
    Handle_Log.Log_Conf(max_bytes=1024)
    for i in range(5):
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')
    logger.debug(Handle_Log.Get_Error())
