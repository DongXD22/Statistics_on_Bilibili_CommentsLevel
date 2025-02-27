from utils import *
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Select_Functions():
    selected_funcs=set()
    _funcs=[getLevelsByComments,getSexByComments,getVipsByComments,getStatesByComments]
    while True:
        func=int(input(
'''
Info you want to know:
1.Levels
2.Sex
3.Vips
4.Hide
5.all
'''))
        if func>0 and func<=4:
            selected_funcs.add(_funcs[func-1])
        elif func==5:
            for f in _funcs:
                selected_funcs.add(f)
        else:
            break

    funcs=[]
    for func in selected_funcs:
        funcs.append(func)
    return funcs

def Settings():
    settings={}
    settings['perpage']=int(input("Get comments every __ page:"))
    settings['target']=int(input(
'''
1.By Video
2.By UserID
'''))
    if settings['target']==1:
        settings['av']=int(input("avid:"))
    else:
        settings['uid']=int(input("uid:"))
        settings['v_num']=int(input("Number of Videos you want (Defult:All) :"))
        if not su:
            su=-1
    return settings
    
def Dev():
    settings={
        'perpage':100,
        'target':1,
        'av':170001,
        'uid':0,
        'v_num':1,
    }
    funcs=[getLevelsByComments,getSexByComments,getVipsByComments,getStatesByComments]
    return funcs,settings

if __name__ == '__main__':
    plt.figure(figsize=(8,8))
    mode=input("1.user 2.dev:")
    if mode=='1':
        funcs=Select_Functions()
        settings=Settings()
    else:
        funcs,settings=Dev()
    if settings['target']==1:
        cmts=getCommentsByVideo(settings['av'],settings['perpage'])
        for i in range(len(funcs)):
            func=funcs[i]
            frm=func(cmts)
            addFrame(frm,i+1)
        plt.suptitle('Info of video:'+str(settings['av']))
    elif settings['target']==2:
        bvs=getVideoByUser(settings['uid'],settings['v_num'])
        frms=[]
        for func in funcs:
            frms.append(func(-1))
        cnt=1
        for bv in bvs:
            print("Geting Comments From Vedio:",cnt,"/",len(bvs))
            cmts=getCommentsByVideo(bv,settings['perpage'])
            cnt+=1
            for i in range(len(funcs)):
                func=funcs[i]
                frms[i]+=func(cmts)
                print(frms[i])
            time.sleep(1)
        for i in range(len(frms)):
            frm=frms[i]
            addFrame(frm,i+1)
        plt.suptitle("Info of User:"+str(settings['uid']))
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


    

