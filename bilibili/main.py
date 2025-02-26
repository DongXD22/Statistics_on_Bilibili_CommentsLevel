from utils import  ShowPie,getCommentsByVideo, getLevelsByComments,getVideoByUser
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
s=int(input('''1.By Video
2.By UserID
'''))
if s==1:
    av=int(input("avid:"))
    cmts=getCommentsByVideo(av)
    lv=getLevelsByComments(cmts)
    frm=pd.Series(lv)
    plt.title("Fans' level of video:"+str(av))
    ShowPie(frm)
elif s==2:
    uid=int(input("uid:"))
    frm=pd.Series(0,index=range(7))
    su=int(input("Number of Videos you want (Defult:All) :"))
    if not su:
        su=-1
    bvs=getVideoByUser(uid,su)
    cnt=1
    for bv in bvs:
        print("Geting Comments From Vedio:",cnt,"/",len(bvs))
        cmts=getCommentsByVideo(bv)
        cnt+=1
        lv=getLevelsByComments(cmts)
        frm+=lv
        print(frm)
        time.sleep(1)
    plt.title("Fans' levels of User:"+str(uid))
    ShowPie(frm)

