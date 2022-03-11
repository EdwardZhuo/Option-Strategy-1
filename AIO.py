# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
import datetime
import math
import pandas as pd


def select_optionAIO(df_so, stockprice_so, callorput_so = 'C', col_callorput_so = 'CallOrPut', col_strike_so = 'ExercisePrice', col_code_so = 'Symbol' ):
    AIO_so = {}
    df1_so = df_so[df_so['%s'%col_callorput_so].isin([callorput_so])]
    df2_so = df1_so.copy()
    df2_so['absgap'] = abs(df2_so['%s'%col_strike_so].astype(float) - stockprice_so)
    df2_so['gap'] = df2_so['%s'%col_strike_so].astype(float) - stockprice_so
    df2_so.sort_values(by = 'absgap',inplace = True)
    AIO_so['ATM'] = df2_so['%s'%col_code_so].tolist()[0]
    df2_so.reset_index(drop=True,inplace=True) 
    df2_so.drop(index=0,inplace=True)
    if callorput_so == 'C':
        df2I_so = df2_so[df2_so['gap'] < 0]
        df2O_so = df2_so[df2_so['gap'] > 0]
        AIO_so['ITM'] = df2I_so['%s'%col_code_so].tolist()
        AIO_so['OTM'] = df2O_so['%s'%col_code_so].tolist()
    elif callorput_so == 'P':
        df2I_so = df2_so[df2_so['gap'] < 0]
        df2O_so = df2_so[df2_so['gap'] > 0]
        AIO_so['ITM'] = df2I_so['%s'%col_code_so].tolist()
        AIO_so['OTM'] = df2O_so['%s'%col_code_so].tolist()
    else:
        print('select option something wrong')
    return AIO_so