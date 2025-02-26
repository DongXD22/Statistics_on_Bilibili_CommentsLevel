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

def getLevelsByComments(comments=-1):
    lvs=pd.Series(0,index=range(7),name='Levels')
    if comments==-1:
        return lvs
    for comment in comments:
        user_level = comment['member']['level_info']['current_level']
        lvs[user_level]+=1
    return lvs

def getSexByComments(comments=-1):
    sex=pd.Series(0,index=['man','woman','secret'],name='Sex')
    if comments==-1:
        return sex
    for comment in comments:
        user_sex=comment['member']['sex']
        if user_sex=='男':
            sex['man']+=1
        elif user_sex=='女':
            sex['woman']+=1
        else:
            sex['secret']+=1
    return sex

def getVipsByComments(comments=-1):
    vips=pd.Series(0,index=['No','Month','Year'],name='Vips')
    if comments==-1:
            return vips
    for comment in comments:
        vip = comment['member']['vip']['vipType']
        vips[vip]+=1
    return vips

def getStatesByComments(comments=-1):
    states=pd.Series(0,index=['Normal','Hide'],name='States')
    if comments==-1:
        return states
    for comment in comments:
        state = comment['state']
        if state:
            states[1]+=1
        else:
            states[0]+=1
    return states

def addFrame(frm,pos):
    plt.subplot(2,2,pos)
    frm=frm[frm>0]
    frm_sum=frm.sum()
    explode=1/(frm/frm_sum)/300
    explode=explode.clip(upper=1)
    plt.pie(frm,startangle=90,explode=explode,autopct='%1.1f%%', labels=frm.index)
    plt.title(frm.name)
    

if __name__ == '__main__':
    cmts=getCommentsByVideo(36676199)
    print ('done')
    lv=getLevelsByComments(cmts)
    print(lv)
    sex=getSexByComments(cmts)
    print(sex)
    st=getStatesByComments(cmts)
    print(st)
    vip=getVipsByComments(cmts)
    print(vip)


    
    
