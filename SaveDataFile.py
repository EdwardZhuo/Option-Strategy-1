# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''

import pandas as pd
import numpy as np
import math


class outputfile:
    def __init__(self):
        globals()['Symbol'] = []
        globals()['Date'] = []
        globals()['TradeTime'] = []
        globals()['StockPrice'] = []
        globals()['Position'] = []
        globals()['Price'] = []
        globals()['Deltacash'] = []
        globals()['Gammacash'] = []
        globals()['Vega'] = []
        globals()['Theta'] = []
        globals()['Margin'] = []
        globals()['Profit'] = []

        globals()['tempposi'] = pd.DataFrame()

    def adddata(self, date0 ='20220117' ,time0 = '093000' ,stockprice0 = 4.800, code0= [], position0 = [],price0 = [],
        deltacash0 = 0.0, gammacash0 = 0.0, vega0 = 0.0, theta0 = 0.0, margin0 = 0.0, profit0 = 0.0):
        globals()['Symbol'].append(code0)
        globals()['Date'].append(date0)
        globals()['TradeTime'].append(time0)
        globals()['StockPrice'].append(stockprice0)
        globals()['Position'].append(position0)
        globals()['Price'].append(price0)
        globals()['Deltacash'].append(deltacash0)
        globals()['Gammacash'].append(gammacash0)
        globals()['Vega'].append(vega0)
        globals()['Theta'].append(theta0)
        globals()['Margin'].append(margin0)
        globals()['Profit'].append(profit0)

    def outputcsv(self, file = 'result'):
        cumprofit = []
        cumprofit0 = 0
        for i in globals()['Profit']:
            cumprofit0 += i
            cumprofit.append(cumprofit0)
        pricechg = [0]
        pricechg0 = 0    
        for i in range(1,len(globals()['StockPrice'])):
            pricechg0 += (globals()['StockPrice'][i]-globals()['StockPrice'][i-1])/globals()['StockPrice'][i-1]
            pricechg.append(pricechg0) 
        resultdict = {
        'Date': globals()['Date'],
        'TradeTime': globals()['TradeTime'],
        'Code': globals()['Code'],
        'StockPrice': globals()['StockPrice'],
        'Pricechg': pricechg,
        'Position': globals()['Position'],
        'Price': globals()['Price'],
        'Deltacash': globals()['Deltacash'],
        'Gammacash': globals()['Gammacash'],
        'Vega': globals()['Vega'],
        'Theta': globals()['Theta'],
        'Margin': globals()['Margin'],
        'Profit': globals()['Profit'],
        'Cumprofit': cumprofit}
        resultdf = pd.DataFrame(resultdict)
        resultdf.to_csv('%s.csv'%file)
    def calprofit(self, dfnew, dfold, stockprice = 0, tradingdate ='20220118' ,tradingtime = '093000', col_new_code = 'newSymbol', col_old_code = 'oldSymbol', 
        col_new_position = 'newposi',col_old_position = 'oldposi', 
        col_new_price = 'newprice', col_old_price = 'oldprice', 
        col_deltacash = 'Deltacash', col_gammacash = 'Gammacash',col_vega = 'Vega', col_theta = 'Theta', 
        col_margin = 'Margin', col_callorput = "CallOrPut", col_multi = "Multiplier", col_fuse = "Fuse",fee = 0.1):

        dfnew[col_old_position] = 0
        dfnew[col_old_price] = 0

        a0 = dfnew[col_new_code].astype(str).tolist()
        a1 = dfnew[col_new_position].astype(float).tolist()
        a2 = dfnew[col_new_price].astype(float).tolist()
        a3 = dfnew[col_old_position].astype(float).tolist() # 0
        a4 = dfnew[col_old_price].astype(float).tolist() # 0

        b0 = dfold[col_new_code].astype(str).tolist()
        b1 = dfold[col_new_position].astype(float).tolist()
        b2 = dfold[col_new_price].astype(float).tolist()


        c1 = pd.Series(a3, index = a0)
        c2 = pd.Series(a4, index = a0)
        d1 = pd.Series(b1, index = b0)
        d2 = pd.Series(b2, index = b0)

        g1 = dfnew[col_deltacash].astype(float).tolist()
        g2 = dfnew[col_gammacash].astype(float).tolist()
        g3 = dfnew[col_vega].astype(float).tolist()
        g4 = dfnew[col_theta].astype(float).tolist()
        m1 = dfnew[col_margin].astype(float).tolist()
        cp = dfnew[col_callorput].astype(str).tolist()
        mu = dfnew[col_multi].astype(float).tolist()
        fu = dfnew[col_multi].astype(str).tolist()

        for i in range(len(b0)):
            tempif0 = float(d1['%s'%b0[i]])
            if abs(tempif0 - 0) < 0.01:
                pass
            else:
                c1['%s'%b0[i]] = tempif0
                c2['%s'%b0[i]] = d2['%s'%b0[i]]

        e1 = list(c1)
        e2 = list(c2)
        newdict = {}
        newdict[col_new_code] = a0 
        newdict[col_new_position] = a1
        newdict[col_new_price] = a2
        newdict[col_old_position] = e1
        newdict[col_old_price] = e2
        newdict[col_deltacash] = g1
        newdict[col_gammacash] = g2
        newdict[col_vega] = g3
        newdict[col_theta] = g4
        newdict[col_margin] = m1
        newdict[col_callorput] = cp
        newdict[col_multi] = mu
        newdict[col_fuse] = fu
        newdf0 = pd.DataFrame(newdict)
        newdf0.set_index(col_new_code, inplace=True, drop=False)
        newdf = newdf0[abs(newdf0[col_new_position]) > 0.1]
        outputfile.exposition(self,newdf)
        feecash = np.abs(np.array(a1) - np.array(e1)) * fee
        feecashsum = feecash.sum()
        netcashtemp = (np.array(a2) - np.array(e2)) * np.array(e1) *  np.array(mu)
        netcash = netcashtemp.sum() - feecashsum
        codetosave = newdf[col_new_code].tolist()
        positiontosave = newdf[col_new_position].tolist()
        pricetosave = newdf[col_new_price].tolist()
        deltacashtosave = 0
        margintosave = 0
        gammacashtosave = 0
        vegatosave = 0
        thetatosave = 0
        profittosave = 0
        for i in range(len(a1)):
            deltacashtosave += a1[i] * g1[i]
            gammacashtosave += a1[i] * g2[i]
            vegatosave += a1[i] * g3[i] * mu[i] / 100.0
            thetatosave += a1[i] * g4[i] * mu[i] / 100.0
        for i in range(len(a1)):
            if a1[i] > 0.01:
                pass
            else:
                margintosave += - a1[i] * m1[i]
        profittosave += netcash
        outputfile.adddata(self, date0 = tradingdate, time0 = tradingtime, stockprice0 = stockprice, 
            code0 = codetosave, position0 = positiontosave,price0 = pricetosave,
            deltacash0 = deltacashtosave, gammacash0 = gammacashtosave, vega0 = vegatosave, theta0 = thetatosave, 
            margin0 = margintosave, profit0 = profittosave)
        return profittosave

    # reset old position 
    def resetexposition(self):
        globals()['tempposi'] = pd.DataFrame()
    # save old position
    def exposition(self, dfpo):
        globals()['tempposi'] = dfpo.copy()
    # get old position
    def getexposi(self):
        return globals()['tempposi']
    # get contracts in oldposition and their position must not be 0.0
    def getexcode(self, col_code = 'newSymbol', col_new_position = 'newposi'):
        temp_gec = globals()['tempposi'][abs(globals()['tempposi']['%s'%col_new_position]) > 0.01]
        return temp_gec[col_code].astype(str).tolist()




