import math
import csv
import sys
import numpy

from scipy.spatial.distance import minkowski
from scipy.spatial.distance import chebyshev
from scipy.spatial.distance import cityblock

emo = dict()
nue_emo_dis = dict()

def euclidean_dis(x,y):
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return distance


def stand_read_csv(fileN):
    with open(fileN) as f:
        reader = csv.reader(f)
        row_n = 1
        for row in reader:
            if row_n == 1:
                pass
            else:
                e = 0
                ang = []
                if row_n >= 2 and row_n <=4:
                    for i in range(0, len(row)):
                        if i >= 3 and i <= 19:
                            e = float(row[i])
                            ang.append(e)

                    if 'ang' in emo:
                        emo['ang'].append(ang)
                    else:
                        emo['ang'] = [ang]
                        #emo['ang'] = ang

                if row_n >= 5 and row_n <= 7:
                    for i in range(0, len(row)):
                        if i >= 3 and i <= 19:
                            e = float(row[i])
                            ang.append(e)

                    if 'hap' in emo:
                        emo['hap'].append(ang)
                    else:
                        emo['hap'] = [ang]

                if row_n >= 8 and row_n <= 10:
                    for i in range(0, len(row)):
                        if i >= 3 and i <= 19:
                            e = float(row[i])
                            ang.append(e)

                    if 'sad' in emo:
                        emo['sad'].append(ang)
                    else:
                        emo['sad'] = [ang]

                if row_n >= 11 and row_n <= 13:
                    for i in range(0, len(row)):
                        if i >= 3 and i <= 19:
                            e = float(row[i])
                            ang.append(e)

                    if 'sur' in emo:
                        emo['sur'].append(ang)
                    else:
                        emo['sur'] = [ang]
                if row_n >=14 and row_n <=16:
                    for i in range(0,len(row)):
                        if i>=3 and i <=19:
                            e = float(row[i])
                            ang.append(e)
                    if "emb" in emo:
                        emo['emb'].append(ang)
                    else:
                        emo['emb'] = [ang]
            row_n = row_n+1

def neut_read_csv(fileN):
    neut_au_mean_list = []
    au1, au2, au4, au5, au6, au7, au9, au10, au12, au14, au15, au17, au20, au23, au25, au26, au45 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    with open(fileN) as f:
        reader = csv.reader(f)
        flag = 1
        for row in reader:
            if flag == 1:
                pass
            else:
                e = 0
                for i in range(0, len(row)):
                    e = float(row[i])
                    if i == 396:
                        au1.append(e)
                    elif i == 397:
                        au2.append(e)
                    elif i == 398:
                        au4.append(e)
                    elif i == 399:
                        au5.append(e)
                    elif i == 400:
                        au6.append(e)
                    elif i == 401:
                        au7.append(e)
                    elif i == 402:
                        au9.append(e)
                    elif i == 403:
                        au10.append(e)
                    elif i == 404:
                        au12.append(e)
                    elif i == 405:
                        au14.append(e)
                    elif i == 406:
                        au15.append(e)
                    elif i == 407:
                        au17.append(e)
                    elif i == 408:
                        au20.append(e)
                    elif i == 409:
                        au23.append(e)
                    elif i == 410:
                        au25.append(e)
                    elif i == 411:
                        au26.append(e)
                    elif i == 412:
                        au45.append(e)

            flag = 0

    neut_au_mean_list = [numpy.mean(au1)]
    neut_au_mean_list.append(numpy.mean(au2))
    neut_au_mean_list.append(numpy.mean(au4))
    neut_au_mean_list.append(numpy.mean(au5))
    neut_au_mean_list.append(numpy.mean(au6))
    neut_au_mean_list.append(numpy.mean(au7))
    neut_au_mean_list.append(numpy.mean(au9))
    neut_au_mean_list.append(numpy.mean(au10))
    neut_au_mean_list.append(numpy.mean(au12))
    neut_au_mean_list.append(numpy.mean(au14))
    neut_au_mean_list.append(numpy.mean(au15))
    neut_au_mean_list.append(numpy.mean(au17))
    neut_au_mean_list.append(numpy.mean(au20))
    neut_au_mean_list.append(numpy.mean(au23))
    neut_au_mean_list.append(numpy.mean(au25))
    neut_au_mean_list.append(numpy.mean(au26))
    neut_au_mean_list.append(numpy.mean(au45))

    return neut_au_mean_list

def calcul_nue_dis(neut_au_mean_list):
    for key in emo.keys():
        nue1_re = [euclidean_dis(neut_au_mean_list, emo[key][0])]
        nue1_re.append(euclidean_dis(neut_au_mean_list, emo[key][1]))
        nue1_re.append(euclidean_dis(neut_au_mean_list, emo[key][2]))
        nue_emo_dis[key] = [nue1_re]
    #print(nue_emo)

def calcul_emotion_dis_csv(fileN):
    ex0 = fileN.split("_")
    ex = ex0[1].split(".csv")
    emotion = ex[0]

    result_dis = dict()

    # 3 standard
    min_dis_st = [9000000 for i in range(3)]

    with open(fileN) as f:
        reader = csv.reader(f)
        flag = 1
        for row in reader:
            if flag == 1:
                pass
            else:
                au = []
                e = 0
                for i in range(0, len(row)):
                    time = (row[1])
                    e = float(row[i])
                    if i >= 396 and i <= 412:
                        au.append(e)

                #find emotion in emo dictionary
                for k in range(0, len(min_dis_st)):
                    st_re = euclidean_dis(au, emo[emotion][k])
                    min_dis_st[k] = min(st_re, min_dis_st[k])

                    if k+1 in result_dis:
                        result_dis[k+1].append(st_re)
                    else:
                        result_dis[k+1] = [st_re]


                #for st_au_list in emo[emotion]:
                #    if 1 in result_dis:

#                    result_dis.append(euclidean_dis(au, st_au_list))
#                    ind += 1

            flag = 0
    return result_dis, min_dis_st


def score_calcul(emo, min_dis_st):
    score = [0 for i in range(3)]

    #print(emo)
    #print(nue_emo_dis[emo])
    nue_dis_list = nue_emo_dis[emo][0]
    #print(nue_dis_list)

    for i in range(0,len(nue_dis_list)):
        #print(nue_emo_dis[emo][i])
        score[i] = ((nue_dis_list[i]-min_dis_st[i])/nue_dis_list[i])*100

    max_score = max(score)

    return score, max_score