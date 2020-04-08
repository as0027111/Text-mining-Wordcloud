# -*- coding: utf-8 -*-
import requests
import json
import os
#import wget
 
#取代違法字源的方法
def text_cleanup(text):
    new =""
    for i in text:
        if i not in'\?.!/;:"':
            new += i
    return new
 
print("開始爬蟲")
 
#偽裝成瀏覽器，(因為Dcard Server有用cloudflare來分流) 沒增加header user-agent 會直接503什麼鬼都看不到
 
header = {
 
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
 
 
# 利用get取得API資料  
url = "https://www.dcard.tw/_api/forums/ncku/posts?popular=false"
reqs = requests.get(url, headers=header)
#print(reqs.status_code) #503 錯誤 // 200等於正常
 
if(int(reqs.status_code)==200):
    print("Dcard伺服器狀態:連線中")
else:
    print("Dcard伺服器狀態:拍謝失敗捏")
    os.system("pause")
    os._exit()
 
 
# 利用json.loads()解碼JSON 
reqsjson = json.loads(reqs.text) 
total_num = len(reqsjson) 
print (total_num) #共30篇

id=[]
context=[]
for i in range(0, 2):
    if(reqsjson[i]["replyId"] == None):#有些是轉貼的
        id.append(reqsjson[i]["id"])
    else:
        id.append(reqsjson[i]["replyId"])
    print(id[i])
    web = "https://www.dcard.tw/_api/posts/"+ str(id[i])
    request=requests.get(web)
    rjson =json.loads(request.text)
    context.append(rjson["content"])
print(context)
#print(corpus)

import jieba
import jieba.analyse
#topK 幾個TF/IDF權重最大的詞, withWeight 是否顯示關鍵詞權重值, allowPOS 指定詞性的詞
print(jieba.analyse.extract_tags(context[1], topK=5, withWeight=True, allowPOS=()))
for x, w in jieba.analyse.extract_tags(context[1], topK=5, withWeight=True):
    print('%s %s' % (x, w))
for x, w in jieba.analyse.textrank(context[1], topK=5, withWeight=True):
    print('%s %s' % (x, w))    
#%%
'''
import jieba
import jieba.analyse
print(jieba.analyse.extract_tags(corpus[0], topK=20, withWeight=False, allowPOS=()))
for x, w in jieba.analyse.extract_tags(corpus[0], withWeight=True):
    print('%s %s' % (x, w))
'''
#TextRank
#for x, w in jieba.analyse.textrank(corpus[0], withWeight=True):
#    print('%s %s' % (x, w))
'''
from sklearn.feature_extraction.text import CountVectorizer
vectoerizer =CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b' )#%%
vectoerizer.fit(corpus)
'''

''' 
for i in range(0,total_num):
    title = reqsjson[i]["title"] #取得每篇標題
    title = text_cleanup(title) #標題會有非法字原要幫她去掉
 
    media_num = len(reqsjson[i]['media']) #判斷這文章圖的數量
    print( title+"檢查有沒有圖檔")
    if media_num != 0:
 
        path =  title #資料夾名字用標題命名
        print("狀態:有圖喔!")
        if not os.path.isdir(path):  #檢查是否已經有了
            os.mkdir(path) #沒有的用標題建立資料夾
        
        for i_m in range(0, media_num):
            image_url = reqsjson[i]['media'][i_m]['url']
 
            filepath =  title + '/' + str(i_m) + '.jpg'
            if not os.path.isfile(filepath): #檢查是否下載過圖片，沒有就下載
                wget.download(image_url, filepath)
                #print(image_url)
    else:
        print("狀態:沒有圖QQ")
'''
print("爬完收工")
