#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv  # 包含CSV库

import jieba
import pandas as pd
import codecs
# 生存 netdraw 数据

names = {}        # 姓名字典
relationships = {} # 关系字典
words = []
freq = open('../../../test/src/data/freq_fix1.csv', 'r')
rows = csv.reader(freq)
for row in rows:
    words.append(row[0])
freq.close();
del words[0]
# print(words)
for w1 in words:
    relationships[w1] = {}

cms = open('../../../test/src/data/comments_fix.csv', 'r')
reader = csv.reader(cms)
for row in reader:
    for w1 in words:
        for w2 in words:
            if w1 == w2:
                continue
            if w1 in row[2] and w2 in row[2]:
                if relationships[w1].get(w2) is None:       # 若尚未同时出现则新建项
                    # print('$$')
                    relationships[w1][w2] = 1
                else:
                    # print('------')
                    relationships[w1][w2] += 1      # 共同出现次数加 1

# output
def save2csv(path, data):
    # 保存文件
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(path, encoding='utf_8_sig', mode='a', index=False, sep=',', header=False)

cList = []
words.insert(0, ' ')
path = '../../../test/src/data/netdraw.csv'
cList.append(words) #第一行

for w in words:
    if not w.isspace():
        tmp = []
        tmp.append(w)
        for _, weight in relationships[w].items():
            tmp.append(weight)
        cList.append(tmp)

save2csv(path, cList)
