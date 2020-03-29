#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv  # 包含CSV库

import jieba
import pandas as pd
import codecs
# 生存 Gephi 数据文件

names = {}        # 姓名字典
relationships = {} # 关系字典
words = []
freq = open('data/freq_fix.csv', 'r')
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
    # if i == 2:
    #     break
    # if i < 2:
    #     i += 1
    #     print(row[2])
    #     print('餐厅' in row[2])
    #     print('玩' in row[2])
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
# print(relationships)
with codecs.open("data/node.csv", "a+", "utf-8") as f:
    f.write("Id Label Weight\r\n")
    freq = open('data/freq_fix.csv', 'r')
    for row in csv.reader(freq):
        f.write(row[0] + " " + row[0] + " " + row[1] + "\r\n")

with codecs.open("data/edge.csv", "a+", "utf-8") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                f.write(name + " " + v + " " + str(w) + "\r\n")
