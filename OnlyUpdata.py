# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
import pandas as pd

def updata(dfdata, dfolddf, 
    col_delta = 'Delta',    
    col_deltacash = 'Deltacash', 
    col_midPrice = 'MidPrice', 
    col_gammacash = 'Gammacash', 
    col_vega = 'Vega', 
    col_theta = 'Theta', 
    col_margin = 'Margin', 
    col_callorput = 'CallOrPut', 
    col_multi = 'Multiplier', 
    col_fuseornot = 'Fuse'):

    newSymbol = []
    newposi = []
    newprice = []
    fuseornot = []
    deltacash = []
    gammacash = []
    vega = []
    theta = []
    thetamargin = []
    callorput = []
    multi = []
    margin = []

    symbollist = dfolddf['newSymbol'].tolist()
    posilist = dfolddf['newposi'].tolist()
    for i in range(len(symbollist)):
        newSymbol.append(symbollist[i])
        newposi.append(posilist[i])
        newprice.append(dfdata.at[symbollist[i], col_midPrice])
        fuseornot.append(dfdata.at[symbollist[i], col_fuseornot])
        deltacash.append(dfdata.at[symbollist[i], col_deltacash])
        gammacash.append(dfdata.at[symbollist[i], col_gammacash])
        vega.append(dfdata.at[symbollist[i], col_vega])
        theta.append(dfdata.at[symbollist[i], col_theta])
        margin.append(dfdata.at[symbollist[i], col_margin])
        callorput.append(dfdata.at[symbollist[i], col_callorput])
        multi.append(dfdata.at[symbollist[i], col_multi])

    dfnewdict = {
        'newSymbol':newSymbol,
        'newposi':newposi,
        'newprice':newprice,
        'Fuse':fuseornot,
        'Deltacash':deltacash,
        'Gammacash':gammacash,
        'Vega':vega,
        'Theta':theta,
        'Margin':margin,
        'CallOrPut':callorput,
        'Multiplier':multi}

    dfnewdf1 = pd.DataFrame(dfnewdict)
    dfnewdf1 = dfnewdf1[abs(dfnewdf1['newposi']) > 0.01]
    print(dfnewdf1)
    return dfnewdf1