#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# QGMA文本管理函数 #
# 作者：稽术宅（funnygeeker）
# QGMA项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/qgma

import chardet  # 文件编码检测，需安装


class Text_Mgt():
    '文本管理'
    def Encodeing_Detect(file_path):
        '文本编码检测，无法识别则默认为"utf-8"编码 返回：str'
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read(1048576))  # 最多读取1MB文件进行检测
            #print(result['confidence'])#
            if float(result['confidence']) >= 0.5:  # 如果置信度大于50%
                return result['encoding'].lower()
            else:
                return 'utf-8'  # 无法识别则默认为"utf-8"编码

    def List_Read_Text(file_path, exclude='', encoding=''):
        '读取文本文件并以列表的形式输出，可选排除某字符开头的行 返回：list'
        if encoding == '':  # 如果没有文本编码参数，则自动识别编码
            encoding = Text_Mgt.Encodeing_Detect(file_path)
        with open(file_path, "r", encoding=encoding) as file:  # 读取文本文件
            all_text = file.readlines()
            if exclude == '':  # 如果不需要排除某字符开头的文本行
                text_list = [text.strip()
                             for text in all_text if text.strip("\n") != ""]
            else:  # 如果需要排除某字符开头的文本行
                text_list = [text.strip() for text in all_text if text.strip(
                    "\n") != "" and text[0] != str(exclude)]
            return text_list

    def Match_List(list, text):
        '逐一匹配列表中的值是否包含在字符串中 返回：bool'
        for item in list:  # 逐一匹配列表
            if str(item) in str(text):  # 如果文本在列表中
                return True
        else:
            return False


if __name__ == '__main__':  # 代码测试
    file_path = './tests/text/test.txt'
    # print(Text_Mgt.Encodeing_Detect(file_path))
    # print(Text_Mgt.List_Read_Text(file_path, '#'))
    # print(Text_Mgt.Match_List(Text_Mgt.List_Read_Text(file_path),'#测试啊'))
