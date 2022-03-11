# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''



import pandas as pd

def initdata(Symbol = [], Position = [], Price = []):
    dfinitdict = {
        'newSymbol':Symbol,
        'newposi':Position,
        'newprice':Price}
    newdf = pd.DataFrame(dfinitdict)
    newdf.set_index('newSymbol',inplace=True, drop=False)
    # print(newdf)
    return newdf

