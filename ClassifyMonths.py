# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
import pandas as pd
import time
import datetime
import warnings

warnings.filterwarnings("ignore")

def classify_month(filepath, day_str_cm = '2022-02-09', col_ExpireDate_cm = 'ExpireDate', newcolED_cm = 'ExpireDays'):
    data_cm = pd.read_excel(filepath)
    day_time_cm = datetime.datetime.strptime(day_str_cm,"%Y-%m-%d")
    listtemp_cm = data_cm['%s'%col_ExpireDate_cm].astype(str).tolist()
    countdays_cm = []
    for i in listtemp_cm:
        time_cm = datetime.datetime.strptime(i,"%Y-%m-%d") - day_time_cm
        countdays_cm.append(time_cm.days)
    data_cm['%s'%newcolED_cm] = countdays_cm
    listType_cm = data_cm['%s'%newcolED_cm].unique()
    listType_cm.sort()
    data_thismonth_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[0]])]
    data_nextmonth_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[1]])]
    data_thisseason_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[2]])]
    # data_nextseason_cm = data_cm[data_cm['%s'%newcolED_cm].isin([listType_cm[3]])]
    return data_thismonth_cm

def selectATM(stockprice,thismonth,col_Symbol = 'Symbol',col_CallOrPut = 'CallOrPut', sign_CP = ['认购','认沽'], col_Strike = 'Strike'):
    
    thismonth_callp = thismonth[thismonth[col_CallOrPut].isin([sign_CP[0]])]
    thismonth_putp = thismonth[thismonth[col_CallOrPut].isin([sign_CP[1]])]
    thismonth_call = thismonth_callp.copy()
    thismonth_put = thismonth_putp.copy()
    thismonth_call['gap'] = thismonth_call[col_Strike].astype(float) - float(stockprice)
    thismonth_put['gap'] = thismonth_put[col_Strike].astype(float) - float(stockprice)
    
    thismonth_call['absgap'] = abs(thismonth_call['gap'])
    thismonth_put['absgap'] = abs(thismonth_put['gap'])
    thismonth_call.sort_values(by = 'absgap',inplace = True)
    thismonth_put.sort_values(by = 'absgap',inplace = True)

    thismonth_call = thismonth_call.iloc[:2]
    thismonth_put = thismonth_put.iloc[:2]
    absgap = thismonth_call['absgap'].astype(float).tolist()

    if absgap[1] - absgap[0] > 0.0001:
        callATMcode = thismonth_call[col_Symbol].astype(str).tolist()[0]
        putATMcode = thismonth_put[col_Symbol].astype(str).tolist()[0]
    else:
        thismonth_call.sort_values(by = 'gap',inplace = True)
        thismonth_put.sort_values(by = 'gap',inplace = True)
        callATMcode = thismonth_call[col_Symbol].astype(str).tolist()[1]
        putATMcode = thismonth_put[col_Symbol].astype(str).tolist()[1]
    return callATMcode, putATMcode

import datetime
import math
import pandas as pd

def select_optionAIO(df_so, stockprice_so, callorput_so = '认购', col_callorput_so = 'CallOrPut', 
    sign_CP = ['认购','认沽'], col_strike_so = 'Strike', col_code_so = 'Symbol' ):

    AIO_so = {}
    df1_so = df_so[df_so['%s'%col_callorput_so].isin([callorput_so])]
    df2_so = df1_so.copy()
    df2_so['absgap'] = abs(df2_so['%s'%col_strike_so].astype(float) - stockprice_so)
    df2_so['gap'] = df2_so['%s'%col_strike_so].astype(float) - stockprice_so
    df2_so.sort_values(by = 'absgap',inplace = True)
    AIO_so['ATM'] = df2_so['%s'%col_code_so].tolist()[0]
    df2_so.reset_index(drop=True,inplace=True) 
    df2_so.drop(index=0,inplace=True)
    if callorput_so == sign_CP[0]:
        df2I_so = df2_so[df2_so['gap'] < 0]
        df2O_so = df2_so[df2_so['gap'] > 0]
        df2I_so.sort_values(by = 'gap',inplace = True) # 从深实至浅实
        df2O_so.sort_values(by = 'gap',inplace = True) # 从浅虚至深虚
        AIO_so['ITM'] = df2I_so['%s'%col_code_so].tolist()
        AIO_so['OTM'] = df2O_so['%s'%col_code_so].tolist()
    elif callorput_so == sign_CP[1]:
        df2I_so = df2_so[df2_so['gap'] < 0]
        df2O_so = df2_so[df2_so['gap'] > 0]
        df2I_so.sort_values(by = 'gap',inplace = True) # 从深虚至浅虚
        df2O_so.sort_values(by = 'gap',inplace = True) # 从浅实至深实
        AIO_so['ITM'] = df2I_so['%s'%col_code_so].tolist()
        AIO_so['OTM'] = df2O_so['%s'%col_code_so].tolist()
    else:
        print('select option something wrong')
    return AIO_so
