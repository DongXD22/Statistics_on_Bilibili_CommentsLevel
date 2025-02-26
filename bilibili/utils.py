import requests
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from DrissionPage import ChromiumPage

def getVideoByUser(uid,num=-1):
    url=f'https://space.bilibili.com/{uid}/video'
    driver =ChromiumPage()
    driver.listen.start('api.bilibili.com/x/space/wbi/arc/search')
    driver.get(url)
    bv=[]
    flag=False
    for page in range(100):
        resp=driver.listen.wait()
        jsondata=resp.response.body
        for index in jsondata['data']['list']['vlist']:
            bv.append(index['aid'])
            if len(bv)==num:
                flag=True
                break
        if flag:
            break
        next_button=driver.ele('@@text()=下一页@@class=vui_button vui_pagenation--btn vui_pagenation--btn-side',timeout=5)
        print ("Got Videos:",len(bv))
        if next_button:
            next_button.click()
        else:
            break
    return bv

def getCommentsByVideo(aid):
    comments=[]
    size=0
    url = "https://api.bilibili.com/x/v2/reply/main"
    params={
        'oid':aid,
        'type':1,
        'next':1,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    while True:
        response = requests.get(url, headers=headers,params=params)
        
        if response.status_code!=200:
            print(response.status_code,response.text)
            return None
        
        data=response.json()
        if data['code']!=0:
            print(data['code'])
            break
        
        cmts=data['data']['replies']
        if not cmts:
            break
        comments.append(cmts)
        size+=len(cmts)
        params['next']+=1
        print ("Got comments",size)
    print ("Done")
    return list(itertools.chain(*comments))

def getLevelsByComments(comments):
    lv=[0,0,0,0,0,0,0]
    for comment in comments:
        user_level = comment['member']['level_info']['current_level']
        lv[user_level]+=1
    return lv

def ShowPie(frm):
    frm=frm[frm>0]
    frm_sum=frm.sum()
    explode=1/(frm/frm_sum)/300
    explode=explode.clip(upper=1)
    frm.plot.pie(autopct='%1.1f%%',explode=explode)
    plt.show()


if __name__ == '__main__':
    bvs=getVideoByUser(208259)
    print (bvs)
    cmts=getCommentsByVideo(bvs[1])
    print ('done')
    lv=getLevelsByComments(cmts)
    print (lv)


    
    
