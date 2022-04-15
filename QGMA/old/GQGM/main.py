#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import os,sys
    os.chdir(sys.path[0]) # 改变程序当前工作路径
    


    #builtins.t1 = 1
    '''
    for temp in os.listdir('./extensions'):
        exec(('from extensions.' + str(temp)).strip('.py') + ' import *')
    '''
    