from utils import *
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
'''))
    if func>0 and func<=4:
        selected_funcs.add(_funcs[func-1])
    else:
        break
    
funcs=[]
for func in selected_funcs:
    funcs.append(func)

s=int(input(
'''
1.By Video
2.By UserID
'''))

if s==1:
    av=int(input("avid:"))
    cmts=getCommentsByVideo(av)
    for i in range(len(funcs)):
        func=funcs[i]
        frm=func(cmts)
        addFrame(frm,i+1)
    plt.suptitle('Info of video:'+str(av))

elif s==2:
    uid=int(input("uid:"))
    su=int(input("Number of Videos you want (Defult:All) :"))
    if not su:
        su=-1
    bvs=getVideoByUser(uid,su)
    cnt=1
    frms=[]
    for func in funcs:
        frms.append(func(-1))
    for bv in bvs:
        print("Geting Comments From Vedio:",cnt,"/",len(bvs))
        cmts=getCommentsByVideo(bv)
        cnt+=1
        for i in range(len(funcs)):
            func=funcs[i]
            frms[i]+=func(cmts)
            print(frms[i])
        time.sleep(1)
    for i in range(len(frms)):
        frm=frms[i]
        addFrame(frm,i+1)
    plt.suptitle("Info of User:"+str(uid))
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()
    

