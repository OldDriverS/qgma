#!/usr/bin/env python
# -*- coding:utf-8 -*-
# https://www.cnblogs.com/xyztank/articles/13599165.html
# https://www.cnblogs.com/pyxiaomangshe/p/7918850.html
# https://blog.csdn.net/qq_36072270/article/details/105345562

#import builtins
from asyncio.log import logger
import os,sys
import traceback
import logging #
import colorlog #
from logging.handlers import RotatingFileHandler

# 日志文件目录处理 #
cur_path = os.path.dirname(os.path.realpath(__file__))# 当前项目路径
log_path = os.path.join(os.path.dirname(cur_path),'logs')# log_path为存放日志的路径，后面的字符串指运行根目录下创建的文件夹名
if not os.path.exists(log_path):# 若不存在logs文件夹，则自动创建
    os.mkdir(log_path)

class Logger(logging.Logger):
    # 日志配置文件 #
    console_log_level = 'DEBUG' # 控制台日志等级
    file_log_level = 'DEBUG' # 文件日志等级
    file_encoding = 'utf-8' # 日志文件编码
    file_max_bytes = 4*1024*1024-1 # 日志文件最大大小
    file_backup_count = 1 # 日志文件拆分次数（0代表1份，1代表两份，以此类推）
    log_file_name = 'QGMA.log' # 日志文件名

    # 终端输出日志颜色配置 #
    log_colors_config = {
        'DEBUG': 'bold_cyan',
        'INFO': 'white',
        'WARNING': 'black,bg_yellow',
        'ERROR': 'black,bg_red',
        'CRITICAL': 'black,bg_purple',
    }
    
    # 日志输出格式设置 #
    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s.%(msecs)03d] -> [%(levelname)s]: \n%(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config
    )
    file_formatter = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d] -> [%(levelname)s]: \n%(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S'
    )

    def __init__(self):
        # BUG file_bytes
        # 输出到控制台
        self.console_handler = logging.StreamHandler()
        # 输出到文件
        self.file_handler = RotatingFileHandler(filename=(log_path+'/'+Logger.log_file_name), mode='a', maxBytes=Logger.file_max_bytes, backupCount=Logger.file_backup_count,  encoding=Logger.file_encoding)
        # 格式化日志
        self.console_handler.setFormatter(Logger.console_formatter)
        self.file_handler.setFormatter(Logger.file_formatter)
        # 配置root logger和日志等级
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 配置控制台和日志文件日志等级
        self.console_handler.setLevel(Logger.console_log_level.upper())
        self.file_handler.setLevel(Logger.file_log_level.upper())
        # 重复日志问题：
        # 1、防止多次addHandler；
        # 2、loggername 保证每次添加的时候不一样；
        # 3、显示完log之后调用removeHandler
        if not self.logger.handlers:
            self.logger.addHandler(self.console_handler)
            self.logger.addHandler(self.file_handler)
        self.console_handler.close()
        self.file_handler.close()

    def debug(self, msg):
        return self.logger.debug(msg)

    def info(self, msg):
        return self.logger.info(msg)

    def warning(self, msg):
        return self.logger.warning(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def critical(self, msg):
        return self.logger.critical(msg)
        
    
    def Get_Error(level=''):
        '获取程序抛出的错误'
        ttype,tvalue,ttraceback = sys.exc_info()
        error_msg = ''
        for temp in traceback.format_tb(ttraceback):
            error_msg += temp
        if 'ERROR' == str.upper(level):
            logging.error(traceback.format_exc())
        else:
            logging.critical(traceback.format_exc())
            quit()

logger=Logger()
'''
# 日志文件名处理 #
log_file_name = str(Logger.log_file_name) # 删除文件名中的不支持符号
for TEMP0 in ['\\', '/', ':', '*', '\"', '<', '>', '|']:
    log_file_name = log_file_name.replace(TEMP0, '')
for TEMP1 in ['', '.', '..']:
    if log_file_name == TEMP1:  # 避免文件名不合法
        log_file_name = 'QGMA.log'
        break
Logger.log_file_name = log_file_name # 应用处理后的文件名
'''
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
%(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
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
'''
# 日志文件名处理 #
        
'''
if __name__ == '__main__': # 代码测试
    Logger.file_max_bytes = 1024
    for i in range(50):
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')
    Logger.console_log_level = 'ERROR'
    for i in range(50):
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')