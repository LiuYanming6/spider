import csv
import jieba

words = {}.fromkeys([line.rstrip() for line in open('../../../test/src/data/negative_words.txt')])
count = 0
with open('../../../test/src/data/comments_fix.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        seg = jieba.cut(row[2])
        for j in seg:
            if j in words:
                count += 1

print(count)