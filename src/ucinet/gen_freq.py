#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv  # 包含CSV库

import jieba
import pandas as pd


# https://github.com/KimMeen/Weibo-Analyst/tree/master/step2_cut_words
# https://github.com/fxsjy/jieba
def save2csv(path, data):
    # 保存文件
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(path, encoding='utf_8_sig', mode='a', index=False, sep=',', header=False)


stopwords = {}.fromkeys([line.rstrip() for line in open('Stopwordfull.txt')])
dict = {}
with open('../../../test/src/data/comments_fix.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # print(row[2])
        seg = jieba.cut(row[2])
        for j in seg:
            if j in stopwords:
                continue
            if (j in dict):
                dict[j] += 1
            else:
                dict[j] = 1

dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)  # 安装value排序
cList = []
path = 'data/freq1718.csv'

for a, b in dict:  # a是中文，b是词出现的次数
    if b > 0:
        tmp = []
        tmp.append(a)
        tmp.append(str(b))
        cList.append(tmp)
save2csv(path, cList)
