# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''

import pandas as pd

def NeedtoHedge(dfdata, code, col_deltacash = 'deltacash', col_position = 'newposi'):
    sum_deltacash = 0
    for i in code:
        sum_deltacash += float(dfdata.at[i, col_deltacash]) * float(dfdata.at[i, col_position])
    return sum_deltacash