# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''

import pandas as pd

def getcsvdata(filepath, csvinput = [0], csvoutput = [0], coltype = [0]):
    csvdata = pd.read_csv(filepath,encoding='gbk')
    k = len(csvinput)
    dictoutput = {}
    for i in range(k):
        if coltype[i] == 'float':
            dictoutput['%s'%csvoutput[i]] = csvdata['%s'%csvinput[i]].astype(float).tolist()
        elif coltype[i] == 'int':
            dictoutput['%s'%csvoutput[i]] = csvdata['%s'%csvinput[i]].astype(int).tolist()
        elif coltype[i] == 'str':
            dictoutput['%s'%csvoutput[i]] = csvdata['%s'%csvinput[i]].tolist()
        else:
            print("import csv data error")
    return dictoutput

