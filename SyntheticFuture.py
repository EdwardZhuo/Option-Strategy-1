# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
import math
import pandas as pd

def synthetic_future(optdata_sf, stockprice_sf, riskfreerate_sf, col_strike_sf = 'BuyPrice01', col_callorput_sf =  'CallOrPut', col_optionprice_sf =  'midPrice', col_expiretime_sf = 'ExpireDays'):

    minday = min(optdata_sf[col_expiretime_sf].astype(float).tolist())

    optdata0_sf = optdata_sf[optdata_sf[col_expiretime_sf].isin([minday])]
    optdata1_sf = optdata0_sf.copy()
    optdata1_sf['gap'] = abs(optdata1_sf[col_strike_sf].astype(float) - float(stockprice_sf))
    optdata1_sf.sort_values(by = 'gap',inplace = True)
    temp_sf = optdata1_sf.iloc[:2]
    target_sf=temp_sf.copy()
    target_sf['CPnum'] = 0
    target_sf.loc[target_sf[col_callorput_sf] == 'P', 'CPnum'] = 1
    target_sf.sort_values(by = 'CPnum',inplace = True)

    target_sf=target_sf.reset_index()

    synf_sf=(float(target_sf[col_optionprice_sf][0])-float(target_sf[col_optionprice_sf][1]))*math.exp(float(riskfreerate_sf)*float(target_sf[col_expiretime_sf][0])/365.0)+float(target_sf[col_strike_sf][0])
    return synf_sf