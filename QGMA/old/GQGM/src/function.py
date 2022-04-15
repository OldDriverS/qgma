#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 用于存放程序常用的基本函数

def Match_List(list, this_Str): # 逐一匹配列表中的值是否包含在字符串中
    for TEMP in list:  # 逐一匹配脏话词库
        if str(TEMP) in str(this_Str):  # 如果检测到了脏话
            return 1
    else:
        return 0