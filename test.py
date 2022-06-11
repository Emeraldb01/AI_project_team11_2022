import csv
import pandas as pd
from csv import reader
from csv import writer
import numpy as np
from numpy import genfromtxt


def test():
    array = np.loadtxt('result.csv', delimiter=',', dtype='str')#將讀取的資料放入array
    array = np.char.split(array)#array切片
    count = 0#計算hit幾次
    tmp = 0#紀錄某些非預期狀況的計數
    list = []#存取判定540手勢開始後，如預期的情形
    time_limit = 0#540手勢開始後的時間限制
    check_5 = 0#確認手勢依序且非變換手勢之誤判
    check_4 = 0#確認手勢依序且非變換手勢之誤判
    check_0 = 0#確認手勢依序且非變換手勢之誤判
    #print(array[0])
    #print(array[1])
    list.append("star")
    lag = 0#觸發540手勢後，在某數字的空窗期計數
    warn = False#警告觸發
    occur = 0
    for i in range(0, len(array[0]) - 1, ):
        occur += 1#發生hit時機
        if (tmp >= 3):#非預期狀況記數超過3，則回歸初始值
            check_5 = 0
            check_4 = 0
            check_0 = 0
            tmp =0
            time_limit = 0
            lag=0
            list.clear()
            list.append("star")
        elif (time_limit>50):#540手勢開始後，若超過約10秒，則下輪回歸初始值(舉例：5~4~0到比完中間到約超過10秒)
            tmp = 3
        elif ((check_4 >= 2) and (array[0][i] == "0" or array[1][i] == "0")):#判定check_4大於等於2(只有一幀可能為誤判)且下個手勢為零
            check_0 +=1
            time_limit += 1
            if(check_0 >=2 ):#手勢為零之值取得滿兩幀，則回歸為初始值
                count += 1#紀錄有幾次hit不須重整為0
                print('hit:'+ str(count)+" Time of occurrence:"+str(round(occur*0.20833,2))+"s"+" spend time:"+str(round(time_limit*0.20833,2))+"s")
                check_5 = 0
                check_4 = 0
                check_0 = 0
                tmp = 0
                time_limit = 0
                lag = 0
                list.clear()
                list.append("star")
            if(count == 3):#hit滿三次則警告觸發，表示超級危險
                warn = True
        elif ((list[len(list)-1]=="4") and (array[0][i] == "5" or array[1][i] == "5")):#手勢變換的非預期狀況
            time_limit += 1
            tmp+=1
        elif ((list[len(list)-1]=="5")and(array[0][i] == "0" or array[1][i] == "0")):#手勢變換的非預期狀況
            time_limit += 1
            tmp += 1
        elif (array[0][i] == "5" or array[1][i] == "5"):#讀取5手勢
            check_5 += 1#記數觸發五幾次
            time_limit += 1
            tmp = 0
            lag = 0
            list.append("5")
        elif (check_5 >= 2)and(array[0][i] == "4" or array[1][i] == "4"):#觸發五滿兩幀且讀取4手勢才算
            time_limit += 1
            check_4 += 1
            tmp = 0
            lag = 0
            list.append("4")
        elif ((list[len(list) - 1] == "4") or (list[len(list) - 1] == "5")) and (array[0][i] == "X" ):
            #lag狀況，假設55554444XXX~，停頓沒比
            lag += 1
            time_limit += 1
            if (lag > 9):#停頓沒比數超過2秒，則下輪直接回歸初始狀態
                tmp = 3
        else:#其他非預期裝況
            time_limit += 1
            tmp += 1

    if(warn):
        print('Attention!')
    elif(count==0):
        print('Safe!')




