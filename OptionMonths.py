# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
import datetime
import math
import pandas as pd

def classify_month(day_str_cm, data_cm, col_ExpireDate_cm = 'ExpireDate', newcolED_cm = 'ExpireDays'):
    day_time_cm = datetime.datetime.strptime(day_str_cm,"%Y%m%d")
    listtemp_cm = data_cm['%s'%col_ExpireDate_cm].astype(str).tolist()
    countdays_cm = []
    for i in listtemp_cm:
        time_cm = datetime.datetime.strptime(i,"%Y%m%d") - day_time_cm
        countdays_cm.append(time_cm.days)
    data_cm['%s'%newcolED_cm] = countdays_cm
    listType_cm = data_cm['%s'%newcolED_cm].unique()
    listType_cm.sort()
    data_thismonth_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[0]])]
    data_nextmonth_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[1]])]
    data_thisseason_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[2]])]
    data_nextseason_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[3]])]
    return data_thismonth_cm, data_nextmonth_cm, data_thisseason_cm, data_nextseason_cm