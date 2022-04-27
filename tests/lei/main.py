import os
import sys
from lei import *
os.chdir(sys.path[0])  # 改变程序当前工作路径
print(Lei.lei)
Lei.lei = 1
print(Lei.lei)
from x import *
print(Lei.lei)