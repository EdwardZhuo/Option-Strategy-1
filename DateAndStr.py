# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
import datetime
import math
import pandas as pd
import time

class date_and_str_output:
    
    def __init__(self, datestr_das):
        self.str = datestr_das
        self.date = datetime.datetime.strptime(self.str,"%Y%m%d%H%M%S")
    def getYYmmddstr_das(self):
        Ymdstr_das = self.date.strftime("%Y%m%d")
        return Ymdstr_das
    def getYYmmstr_das(self):
        Ymstr_das = self.date.strftime("%Y%m")
        return Ymstr_das
    def getHHMMSSdatecolon_das(self, HMSstr_das = '0'):
        if HMSstr_das == '0':
            HMSstr_das = self.date.strftime("%H%M%S")
            HMScolonstr_das =  "%s:%s:%s"%(HMSstr_das[:2], HMSstr_das[2:4], HMSstr_das[4:])
            HMSdatecolon_das = datetime.datetime.strptime(HMScolonstr_das,"%H:%M:%S")
            return HMSdatecolon_das
        else:
            HMScolonstr_das =  "%s:%s:%s"%(HMSstr_das[:2], HMSstr_das[2:4], HMSstr_das[4:])
            HMSdatecolon_das = datetime.datetime.strptime(HMScolonstr_das,"%H:%M:%S")
            return HMSdatecolon_das
    def n_mimutes(self, nm_das):
        n_m_das = datetime.timedelta(minutes = nm_das)
        return n_m_das 
    def n_days(self, nd_das):
        n_d_das = datetime.timedelta(days = nd_das)
        return n_d_das