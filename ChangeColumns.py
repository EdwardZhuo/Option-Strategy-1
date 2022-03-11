# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''

import pandas as pd


    
def Chg_col(dfdata, oldcol = [], newcol = []):
    n = len(oldcol)
    for i in range(n):
        old = oldcol[i]
        new = newcol[i]
        dfdata.rename(columns={old:new},inplace=True)
    return dfdata

# dfdata = pd.DataFrame({'A':[1,2,3],'B':[4,5,6],'C':[7,8,9]})
# print(dfdata)
# dfdata1 = Chg_col(dfdata, oldcol = ['A','B'], newcol = ['a','b'])
# print(dfdata1)

