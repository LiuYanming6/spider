import requests
import json
import pandas as pd
import os

# https://cruise.ctrip.com/poi/rci-spectrum_of_the_seas/comment.html
def saveCmts(path, filename, data):
    # 如果路径不存在，就创建路径
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(path + filename, encoding='utf_8_sig', mode='a', index=False, sep=',', header=False )

def fetch(index):

    url = "https://cruise.ctrip.com/ajax/getcommentjson"
    headers = {
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://cruise.ctrip.com',
        'Referer': 'https://cruise.ctrip.com/poi/rci-spectrum_of_the_seas/comment.html',
        'accept': 'text/plain, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
                'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
                'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }

    formData = {
        'PageIndex': index,
        'VoyaID': '0',
        'Section': 'All',
        'ShipID': '474',
        'NeedCount': 'true',
        'PageSize': '1000'
    }

    # 发起网络请求
    r = requests.post(url, data=formData,headers=headers)
    r.raise_for_status()
    # r.encoding = r.apparent_encoding 加上乱码

    # 打印 r.text 来看看是否获取到了数据
    print(r.text)
    print(len(r.text))
    
    # 解析 json 文件，提取数据
    json_data = json.loads(r.text)['Comments']
 
    cList = []
    for item in json_data:
        date = item['Comment']['CommentDate']
        # print(date, item['ProductScore']['Score'], item['Comment']['CommentContent'])
        cmt = []
        scores = [item['ProductScore']['Score'],item['ProductScore']['ServiceScore'],item['ProductScore']['ResturantmentScore'],item['ProductScore']['EnterainmentScore'],item['ProductScore']['RecommendationScore']]

        cmt.append(item['Comment']['CommentDate'])
        cmt.append(scores)
        cmt.append(item['Comment']['CommentContent'])

        cList.append(cmt)
    print(len(cList))
    return cList


path = '../../../test/src/data/'
filename = 'comments_fix.csv'
cmts = fetch('1')
saveCmts(path, filename, cmts)
cmts = fetch('2')
saveCmts(path, filename, cmts)
