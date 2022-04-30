#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 用于存放“设置管理”相关函数
import os
import chardet # 文件编码检测，需安装
#from src.log import *
from configobj import ConfigObj # 配置文件管理，需安装

def Check_File(): # 检查文件是否存在，不存在则创建文件
    for temp in range(2):
        if os.path.isfile("./settings.txt") == True:
            if os.access("./settings.txt", os.R_OK): # 检查文件是否可读
                return 0
            else:
                print('错误：./settings.txt文件不可读')
                quit()
            
        else:
            print('settings.txt文件不存在，即将尝试创建settings.txt')
            Write_Settings_File()

    else:
        print('./settings.txt文件异常，具体错误未知！')

def Load_Settings(): # 加载设置文件
    global settings
    settings = ConfigObj('./settings.txt', encoding='utf-8')


def Check_Settings():
    pass#TODO

def Encodeing_detect(file_path):
    with open(file_path, 'rb') as temp:
        return chardet.detect(temp.read(1024000))["encoding"]

def Write_Settings_File():
    with open('./settings.txt', 'w', encoding='utf-8') as temp:
        temp.write('''# 扩展设置 #
[extensions]
# 需要启用的扩展的扩展名，每项用空格隔开
extensions_name = gqgm

# GO-CQHTTP服务配置 #
# 不懂则不需要修改
[connect]
# GO-CQHTTP服务器的IP地址
server_addr = 127.0.0.1
# GO-CQHTTP的API通信端口
server_api_port = 5701
# GO-CQHTTP的事件监听端口
server_event_port = 5700

# DEBUG设置 #
# 不懂则不需要修改
[debug]
# 接收消息时打印消息原始数据
# 0表示不启用，1表示启用
print_rev = 0
# 日志文件在可执行文件同一目录的logs文件夹下
# 日志文件名称
log_file_name = gqapi.log
# 日志等级：(1-5)debug,info,warning,error,critical
# 日志模块加载完成前，无法正常输出日志
# 写入日志文件的日志等级
file_log_level = 2
# 输出到控制台的日志等级
console_log_level = 2''')
#Check_File()
#Load_Settings()

if __name__ == '__main__':
    print(Encodeing_detect('./settings.txt'))
    