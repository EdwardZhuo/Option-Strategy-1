# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''

import pandas as pd

class NewPosition():
    def __init__(self):
        self.newSymbol = []
        self.newposi = []
        self.newprice = []
        self.fuseornot = []
        self.deltacash = []
        self.gammacash = []
        self.vega = []
        self.theta = []
        self.margin = []
        self.callorput = []
        self.multi = []
    def adddata(self, code = 0, newSymbol0 = 0, newposi0 = 0, newprice0 = 0, fuseornot0 = 0, 
        deltacash0 = 0, gammacash0 = 0, vega0 = 0, theta0 = 0, 
        margin0 = 0 ,callorput0 = 0 ,multi0 = 0):
        self.newSymbol.append(newSymbol0)
        self.newposi.append(newposi0)
        self.newprice.append(newprice0)
        self.fuseornot.append(fuseornot0)
        self.deltacash.append(deltacash0)
        self.gammacash.append(gammacash0)
        self.vega.append(vega0)
        self.theta.append(theta0)
        self.margin.append(margin0)
        self.callorput.append(callorput0)
        self.multi.append(multi0)
    def adddataforneu(self, dfdata, newSymbol = 0, newposi = 0, col_newprice = 'midPrice', 
        col_fuseornot = 'fuseornot', col_deltacash = 'deltacash', col_gammacash = 'gammacash', 
        col_vega = 'vega', col_theta = 'theta', 
        col_margin = 'MarginUnit' ,col_callorput = 'CallOrPut' ,col_multi = 'ContractMultiplierUnit' ):
        self.newSymbol.append(newSymbol)
        self.newposi.append(newposi)
        self.newprice.append(dfdata.at[newSymbol, col_newprice])
        self.fuseornot.append(dfdata.at[newSymbol, col_fuseornot])
        self.deltacash.append(dfdata.at[newSymbol, col_deltacash])
        self.gammacash.append(dfdata.at[newSymbol, col_gammacash])
        self.vega.append(dfdata.at[newSymbol, col_vega])
        self.theta.append(dfdata.at[newSymbol, col_theta])
        self.margin.append(dfdata.at[newSymbol, col_margin])
        self.callorput.append(dfdata.at[newSymbol, col_callorput])
        self.multi.append(dfdata.at[newSymbol, col_multi])
    def getnewdf(self):
        dfnewdict = {
        'newSymbol':self.newSymbol,
        'newposi':self.newposi,
        'newprice':self.newprice,
        'fuseornot':self.fuseornot,
        'deltacash':self.deltacash,
        'gammacash':self.gammacash,
        'vega':self.vega,
        'theta':self.theta,
        'margin':self.margin,
        'callorput':self.callorput,
        'multi':self.multi
        }
        dfnewdf = pd.DataFrame(dfnewdict)
        return dfnewdf


