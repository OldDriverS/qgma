#!/usr/bin/env python
# encoding: utf-8


if __name__ == '__main__':
    import os,sys
    os.chdir(sys.path[0]) # 改变程序当前工作路径

from connect.receive import *
from time import time

import re
import jieba #需要安装
from nltk.classify import NaiveBayesClassifier #需要安装


"""
#Author: 香菜
@time: 2021/8/5 0005 下午 9:29
"""
rule = re.compile(r"[^a-zA-Z\u4e00-\u9fa5]")
def delComa(text):
    text = rule.sub('', text)
    return text
def loadData(fileName):
    text1 = open(fileName, "r", encoding='utf-8').read()
    text1 = delComa(text1)
    list1 = jieba.cut(text1)
    return " ".join(list1)

# 特征提取
def word_feats(words):
    return dict([(word, True) for word in words])

def train_decision():
    global classifier
    adResult = loadData(r"ads.txt")
    yellowResult = loadData(r"d.txt")
    normalResult = loadData(r"normal.txt")
    ad_features = [(word_feats(lb), 'ad') for lb in adResult]
    yellow_features = [(word_feats(df), 'ye') for df in yellowResult]
    normalResult_features = [(word_feats(nl), 'no') for nl in normalResult]
    train_set = ad_features + yellow_features + normalResult_features

    start_time = int(time())
    # 训练决策
    classifier = NaiveBayesClassifier.train(train_set)
    print('用时：',str((int(time())-start_time)))

def send_msg(msg):
    import requests # 需要安装
    try:res=requests.post(url='http://127.0.0.1:5700/send_group_msg', data={"group_id":'1027033288','message':msg})
    except ConnectionError:print('error')
    print(str(res))

def analysis_test(sentence):
    # 分析测试
    #sentence = input("请输入一句话：")
    sentence = delComa(sentence)
    print("\n")
    seg_list = jieba.cut(sentence)
    result1 = " ".join(seg_list)
    words = result1.split(" ")
    print(words)
    # 统计结果
    ad = 0
    yellow = 0
    normal = 0
    for word in words:
     classResult = classifier.classify(word_feats(word))
     if classResult == 'ad':
        ad = ad + 1
     if classResult == 'ye':
        yellow = yellow + 1
     if classResult == 'no':
        normal += 1
    # 呈现比例
    x = float(str(float(ad) / len(words)))
    y = float(str(float(yellow) / len(words)))
    z = float(str(float(normal) / len(words)))
    if len(words) <= 1 and len(words[0]) <= 1:
        #ad = yellow = 0
        x = y = 0
        z = 1
    ad_end = '广告的可能性：%.2f%%' % (x * 100)
    dirty_end = '脏话的可能性：%.2f%%' % (y * 100)
    normal_end = '正常的可能性：%.2f%%' % (z * 100)
    end_info = ad_end + '\n' + dirty_end + '\n' + normal_end
    #print(end_info)
    print(str(words)+'\n'+end_info+'\nAD:'+str(ad)+'\nBAD:'+str(yellow)+'\nNO:'+str(normal))
    global mode1
    if mode1 == 1:
        send_msg(str(words)+'\n'+end_info+'\nAD:'+str(ad)+'\nBAD:'+str(yellow)+'\nNO:'+str(normal))

if __name__ == '__main__':
    train_decision()
    mode0 = input('MODE:')
    mode1 = 0
    if mode0 == '1':
        mode1 = 1
        while 1:
            try:
                rev = rev_msg()
                if rev == None:
                    continue
            except:
                continue
            if (rev["post_type"] == "message") and (rev["message_type"] == "group") and ('1027033288'== str(rev['group_id'])):
                analysis_test(rev['message'])
    elif mode0 == '2':
        while 1:
            try:
                rev = rev_msg()
                if rev == None:
                    continue
            except:
                continue
            if (rev["post_type"] == "message") and (rev["message_type"] == "group") and ('1027033288'== str(rev['group_id'])):
                analysis_test(rev['message'])
    else:
        while 1:
            analysis_test(input('IN:'))