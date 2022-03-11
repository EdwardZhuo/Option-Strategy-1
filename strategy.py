# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''

import math
import pandas as pd
from pulp import *

def optimalneturalstrategy(hedgecode = [], deltacashlist = [], marginlist =[], 
    unchangeddeltacash = 0.0, unchangedmargin = 0.0, maxmargin = 4000000.0 ,
    maxdelta = 1750000.0, mindelta = -300000.0, numITM = 210.0):

    n = len(hedgecode)
    if n == 1:
        perfectnum = (unchangeddeltacash - (maxdelta / 2.5)) / deltacashlist[0]
        variablesvaluedict = {}
        variablesvaluedict['%s'%hedgecode[0]] = int(perfectnum)   
        return variablesvaluedict
    elif n == 2:
        prob = LpProblem('myPro', LpMinimize)
        x0 = LpVariable("x0", lowBound=0)
        x1 = LpVariable("x1", lowBound=0)

        deltaratio = deltacashlist[0] / deltacashlist[1] 
        minnum = (unchangeddeltacash - (maxdelta / 2.5)) / deltacashlist[0]
        maxnum = (unchangeddeltacash - (maxdelta / 2.5)) / deltacashlist[1]

        prob += -x0 * deltacashlist[0] - x1 * deltacashlist[1] + unchangeddeltacash - (maxdelta / 2.5)

        prob +=  -x0 * deltacashlist[0] - x1 * deltacashlist[1] + unchangeddeltacash - (maxdelta / 2.5) >= -50000.0
        prob +=  -x0 * deltacashlist[0] - x1 * deltacashlist[1] + unchangeddeltacash - (maxdelta / 2.5) <= 50000.0
  
        prob += x0  + x1 <= maxnum
        prob += x0  + x1 >= minnum
        prob += x0  - x1 * deltaratio == 0
    

        prob +=  x0 * marginlist[0] + x1 * marginlist[1] + unchangedmargin <= maxmargin

        prob.solve()
        variablesvaluedict = {}
        for i,j in zip(prob.variables(),range(n)):
            variablesvaluedict['%s'%hedgecode[j]] = int(i.varValue)  
        return variablesvaluedict
    else:
        print("PULP something wrong")
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
    def adddataforneu(self, dfdata, newSymbol = 0, newposi = 0, col_newprice = 'MidPrice', 
        col_fuseornot = 'Fuse', col_deltacash = 'Deltacash', col_gammacash = 'Gammacash', 
        col_vega = 'Vega', col_theta = 'Theta', 
        col_margin = 'Margin' ,col_callorput = 'CallOrPut' ,col_multi = 'Multiplier' ):
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
        'Fuse':self.fuseornot,
        'Deltacash':self.deltacash,
        'Gammacash':self.gammacash,
        'Vega':self.vega,
        'Theta':self.theta,
        'Margin':self.margin,
        'CallOrPut':self.callorput,
        'Multiplier':self.multi
        }
        dfnewdf = pd.DataFrame(dfnewdict)
        return dfnewdf



def netural_strategy(dfdata, dfolddf, 
    col_delta = 'Delta',    
    col_deltacash = 'Deltacash', 
    col_midPrice = 'MidPrice', 
    col_gammacash = 'Gammacash', 
    col_vega = 'Vega', 
    col_theta = 'Theta', 
    col_margin = 'Margin', 
    col_callorput = 'CallOrPut', 
    col_multi = 'Multiplier', 
    col_fuseornot = 'Fuse',
    ITMcodep = [],
    AOTMcodep = [],
    fuselist = [],
    maxmarginp = 4000000.0, 
    maxdeltap = 1750000.0, 
    mindeltap = -300000.0):

    newdata = NewPosition()

    dfbuy = dfolddf[dfolddf['newposi'] > 0.1]
    dfsell = dfolddf[dfolddf['newposi'] < -0.1]
    buylist = list(dfbuy.index)
    selllist = list(dfsell.index)
    buyposilist = list(dfbuy['newposi'])
    sellposilist = list(dfsell['newposi'])


    
    


    buydeltasum = 0
    buyposisum = 0
    buydeltacashsum = 0
    buymargin = 0

    numbuycode = len(buylist)
    if numbuycode < 1.01:
        if buylist[0] in fuselist: 
            buydeltacashsum += dfdata.at[buylist[0], col_deltacash] * buyposilist[0]
            buymargin += dfdata.at[buylist[0], col_midPrice] * buyposilist[0] * dfdata.at[buylist[0], col_multi]
            newdata.adddataforneu(dfdata, newSymbol = buylist[0], newposi = buyposilist[0])
        else: 
            buydeltasum = dfdata.at[buylist[0], col_delta] * buyposilist[0]
            buyposisum = buyposilist[0] 
            buydelta = buydeltasum / buyposisum
            # print(buydeltasum)
            # print(buyposisum)
            # print(buydelta)
            if buydelta - 0.7 > 0.00001: 
                for i in range(numbuycode):
                    buydeltacashsum += dfdata.at[buylist[i], col_deltacash] * buyposilist[i]
                    buymargin += dfdata.at[buylist[i], col_midPrice] * buyposilist[i] * dfdata.at[buylist[i], col_multi]
                    newdata.adddataforneu(dfdata, newSymbol = buylist[i], newposi = buyposilist[i])
            elif buydelta - 0.7 < 0.00001: 
                ITMcodep.reverse()
                a0 = dfdata.at[ITMcodep[0], col_delta] 
                a1 = dfdata.at[ITMcodep[1], col_delta]
                a2 = dfdata.at[ITMcodep[2], col_delta] 
                amax = max(a0,a1,a2)               
                if amax < 0.8001 : 
                    print('no proper buycode')
                    for i in range(numbuycode):
                        buydeltacashsum += dfdata.at[buylist[i], col_deltacash] * buyposilist[i]
                        buymargin += dfdata.at[buylist[i], col_midPrice] * buyposilist[i] * dfdata.at[buylist[i], col_multi]
                        newdata.adddataforneu(dfdata, newSymbol = buylist[i], newposi = buyposilist[i])
                else: 
                    temp = 0.0
                    for i in ITMcodep:                        
                        if temp < 0.01 :                            
                            newbuydelta = dfdata.at[i, col_delta]                            
                            if newbuydelta > 0.8000 :                            
                                buydeltacashsum += dfdata.at[i, col_deltacash] * buyposisum
                                buymargin += dfdata.at[i, col_midPrice] * buyposisum * dfdata.at[i, col_multi] 
                                newdata.adddataforneu(dfdata, newSymbol = i, newposi = buyposisum)
                                temp = 1.0                            
                            else:                                
                                pass                        
                        else:                            
                            pass
    else:
        print("buy code something wrong")

    deltacashtohedge = buydeltacashsum 
    selldeltacashsum = 0.0

    for i in range(len(selllist)):
        selldeltacashsum += dfdata.at[selllist[i], col_deltacash] * sellposilist[i]

    deltacashsum = selldeltacashsum + buydeltacashsum
    print(deltacashsum)
    if deltacashsum > maxdeltap or deltacashsum < mindeltap:
        
        flitercode = []
        for i in AOTMcodep:
            if dfdata.at[i, col_midPrice] > 0.01:
                flitercode.append(i)
            else:
                pass
        
        hedgecode0 = []
        numflitercode = len(flitercode)
        if numflitercode > 2.001:
            hedgecode0 = flitercode[1:]
        elif numflitercode > 0.001:
            hedgecode0 = flitercode
        else:
            print('0 sell code')

        hedgecode = []
        for i in hedgecode0:
            if i in fuselist:
                pass
            else:
                hedgecode.append(i)
        n_hc = len(hedgecode0)-len(hedgecode)
        hedgecodefuse = []
        for i in hedgecode0:
            if i in hedgecode:
                pass
            else:
                hedgecodefuse.append(i)
        hf = len(hedgecodefuse)
        h0 = len(hedgecode0)
        
        deltacashlist = []
        marginlist = []
        if h0 - hf > 0.01:
            for i in hedgecode:
                deltacashlist.append(dfdata.at[i, col_deltacash])
                marginlist.append(dfdata.at[i, col_margin])
            
            marginsum = buymargin
            if h0 < 0.01:
                pass
            else:
                for i in hedgecodefuse:
                    if i in selllist:
                        ind = selllist.index(i)
                        deltacashtohedge += dfdata.at[i, col_deltacash] * sellposilist[ind]
                        marginsum += dfdata.at[i, col_margin] * ( - sellposilist[ind]) 
                        newdata.adddataforneu(dfdata, newSymbol = i, newposi = sellposilist[ind])
                    else:
                        pass
            print(hedgecode, deltacashlist, marginlist,deltacashtohedge,marginsum,maxmarginp,maxdeltap,mindeltap,buyposisum)
            resultdict = optimalneturalstrategy(hedgecode = hedgecode, deltacashlist = deltacashlist, marginlist = marginlist, 
            unchangeddeltacash = deltacashtohedge, unchangedmargin = marginsum, maxmargin = maxmarginp, 
            maxdelta = maxdeltap, mindelta = mindeltap, numITM = buyposisum)
            print(resultdict)
            for i in range(len(hedgecode)):
                # print(resultdict[hedgecode[i]])
                temprposi = 0.0 - float(resultdict[hedgecode[i]])
                newdata.adddataforneu(dfdata, newSymbol = hedgecode[i], newposi = temprposi)
        elif h0 - hf < 0.01:
            for i in range(len(selllist)):
                newdata.adddataforneu(dfdata, newSymbol = selllist[i], newposi = sellposilist[i])
            print("all sellcode fuse")
        else:
            print("fuse code something wrong")

    else:
        for i in range(len(selllist)):
            newdata.adddataforneu(dfdata, newSymbol = selllist[i], newposi = sellposilist[i])
    
    
    dfnewdf = newdata.getnewdf()
    oldsymbollist = dfolddf['newSymbol'].tolist()
    newsymbollist = dfnewdf['newSymbol'].tolist()
    for i in oldsymbollist:
        if i in newsymbollist:
            pass
        else:
            newdata.adddataforneu(dfdata, newSymbol = i, newposi = 0)
    dfnewdf = newdata.getnewdf()
    return dfnewdf

