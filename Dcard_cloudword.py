# -*- coding: utf-8 -*-
import requests
import json
import os
import pandas as pd
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
#ncku
url = "https://www.dcard.tw/_api/forums/ncku/posts?popular=true"
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
for i in range(0, 1):
    if(reqsjson[i]["replyId"] == None):#有些是轉貼的
        id.append(reqsjson[i]["id"])
    else:
        id.append(reqsjson[i]["replyId"])
    print(id[i])
    web = "https://www.dcard.tw/_api/posts/"+ str(id[i])
    request=requests.get(web)
    rjson =json.loads(request.text)
    context.append(rjson["content"])
print(context[0])

#%%
import jieba
import jieba.analyse
# 停留詞詞庫
# https://raw.githubusercontent.com/tomlinNTUB/Python/master/%E4%B8%AD%E6%96%87%E5%88%86%E8%A9%9E/%E5%81%9C%E7%94%A8%E8%A9%9E.txt
stopword_txt= './stop_word.txt'
jieba.analyse.set_stop_words(stopword_txt)

def remove_stop_words(file_name,seg_list):
    with open(file_name,'r',encoding="utf-8") as f:
        stop_words = f.readlines()

#stop_words += ['\n'] # rstrip會剔除掉，所以補一個回去
    stop_words = [stop_word.rstrip() for stop_word in stop_words]
    new_list = []
    for seg in seg_list:
        if seg not in stop_words:
            new_list.append(seg) #若在for loop裡用remove的話則會改變總長度
    return new_list

def count_segment_freq(seg_list):
    seg_df= pd.DataFrame(seg_list, columns=['seg'])
    seg_df['count']=1
    seg_freq= seg_df.groupby('seg')['count'].sum().sort_values(ascending=False)
    seg_freq= pd.DataFrame(seg_freq)
    return seg_freq
#%%
#context[0] ='氣象局指出，今天（15日）在西南風影響下，清晨至上午中南部沿海會有零星短暫陣雨，其他地區上半天雖然大致維持多雲到晴，不過由於環境水氣增多，天氣趨於不穩定，午後雷陣雨範圍將會擴大，除東半部地區及西半部山區外，大台北地區及西半部山區附近平地也有午後雷雨發生的機率，午後對流出現的時間會比較早，降雨有機會持續到晚上，並且局部地區也有短時強降雨發生的機率，請多留意午後天氣的變化。溫度方面，各地白天暖熱，高溫普遍約30到33度，南部近山區平地有機會出現36度以上高溫，中午前後請多補充水分及做好防曬措施，而各地夜晚及清晨低溫普遍在22至25度之間，相對舒適許多'
seg_list=jieba.cut(context[0], cut_all=False)
print(seg_list)
for seg in seg_list:
  print(seg,end=' ')
print('')

seg_list = jieba.lcut(context[0], cut_all=False)

# 移除停留詞
seg_list= remove_stop_words(stopword_txt, seg_list)
print("stop word remove")
print(seg_list)

seg_frequency = count_segment_freq(seg_list)
print("frequency:")
print(seg_frequency.head(5))
#%% wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import imageio
import matplotlib.pyplot as plt

font_path = './kaiu.ttf' #標楷體
seg_list=' '.join(seg_list) #將所有陣列中的元素轉成字串型態後，連接合併成一個字串

back_img = imageio.imread('./Dcard.jpg')
wc = WordCloud(
    background_color='white',
    max_words=100,     # 最大詞數
    mask=back_img,
    #max_font_size=90, # 字體的最大值
    #stopwords=STOPWORDS.add("我好棒"),
    random_state=10,
    font_path=font_path,
    prefer_horizontal=0.9 #  調整詞雲中字體水平和垂直的多少
    )
wc.generate(seg_list)
#手動背景圖片-用圖片色彩為文字色彩
image_colors = ImageColorGenerator(back_img)
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
plt.show()
fig_path = './text.png'
wc.to_file(fig_path)

'''
#topK 幾個TF/IDF權重最大的詞, withWeight 是否顯示關鍵詞權重值, allowPOS 指定詞性的詞
print(jieba.analyse.extract_tags(context[1], topK=5, withWeight=True, allowPOS=()))
for x, w in jieba.analyse.extract_tags(context[1], topK=5, withWeight=True):
    print('%s %s' % (x, w))
for x, w in jieba.analyse.textrank(context[1], topK=5, withWeight=True):
    print('%s %s' % (x, w))    
'''