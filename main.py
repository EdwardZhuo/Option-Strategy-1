from iFinDPy import *
import pandas as pd
import numpy as np
from datetime import datetime
import time
import math


from Greeks import *
from SyntheticFuture import *
from Ifind import *
from ChangeColumns import *
from PositionCsv import *
from InitiatePosition import *
from SaveDataFile import *
from strategy import *
from Fuse import *
from ClassifyMonths import *





def add_col(dfdata1,dfdata2):
    # insert new column "CallOrPut" & 'Margin'
    Code = dfdata1['Code'].tolist()
    CallOrPut = []
    for i in range(len(Code)):
        CallOrPut.append(Code[i][6])
    dfdata1['CallOrPut'] = CallOrPut
    dfdata1['Margin'] = 0.0
    # insert new column "Fuse","MidPrice"
    bid1 = dfdata2['Bid1'].tolist()
    ask1 = dfdata2['Ask1'].tolist()
    fuse = []
    midprice = []
    for i in range(len(bid1)):
        mprice = (bid1[i] + ask1[i]) / 2.0
        midprice.append(mprice)
        if abs(bid1[i] - ask1[i]) < 0.000001:
            fuse.append('yes')
        else:
            fuse.append('no')
    dfdata2['Fuse'] = fuse
    dfdata2['MidPrice'] = midprice
    dfdata = pd.merge(dfdata1,dfdata2,on = 'Symbol').dropna(axis=0)
    return dfdata 
def timecount():
    curr_time = datetime.datetime.now()
    time_str = curr_time.strftime("%H:%M:%S")
    return time_str
def newdata(Symbol0,callatm,putatm):
    Symbollist = []
    Symbollist.append(callatm)
    Symbollist.append(putatm)
    Symbollist += Symbol0
    Symbollist = list(set(Symbollist))
    SymbolForIfind = ''
    for i in Symbollist:
        SymbolForIfind = SymbolForIfind + str(i) + '.SH,'
    SymbolForIfind = SymbolForIfind[:-1]
    # print(SymbolForIfind)
    basicinfo = getmarketdata.get_option_data_BD(
        SymbolForIfind,
        'ths_option_code_option;ths_strike_price_option;ths_contract_multiplier_option;ths_surplus_duration_calendar_option',
        ';;;')
    basicinfo = Chg_col(basicinfo, 
        oldcol = ['thscode','ths_option_code_option','ths_strike_price_option','ths_contract_multiplier_option','ths_surplus_duration_calendar_option'], 
        newcol = ['Symbol','Code','Strike','Multiplier','ExpireDays'])
    marketdata0 = getmarketdata.get_option_data(
        SymbolForIfind, 
        'tradeTime;latest;bid1;ask1')
    stockdata =  getmarketdata.get_stockprice_data(
        '510300.OF', 
        'tradeTime;preClose;latest')
    marketdata0 = Chg_col(marketdata0, 
        oldcol = ['thscode','tradeTime','latest','bid1','ask1'],
        newcol = ['Symbol','TradeTime','Latest','Bid1','Ask1'])
    # print(marketdata0)
    stockprice = max(stockdata.latest)
    neu1 = add_col(basicinfo,marketdata0)
    # print(basicinfo)
    # print(marketdata0)
    # print(neu1)
    # clean data for synf
    synprice = synthetic_future(neu1, stockprice, 0.02, col_strike_sf = 'Strike', 
        col_callorput_sf =  'CallOrPut', col_optionprice_sf =  'MidPrice', col_expiretime_sf = 'ExpireDays')
    data_greeks = get_greeks(neu1, synprice, 0.02, 0.00,
        cpsign_gg = ['C','P'],
        listcol_gg = ['Strike','ExpireDays','CallOrPut','MidPrice','Multiplier'])
    # data_greeks.to_csv('greeks.csv')
    data_greeks.set_index('Symbol',inplace=True, drop=False)
    return data_greeks, stockprice

csvdict = getcsvdata(r'position.csv', 
    csvinput = ['代码','持仓','阈值'], 
    csvoutput = ['Symbol','Position','threshold'], 
    coltype = ['str','int','int'])
Symboli = csvdict['Symbol']
Symbol0 = [str(x) for x in Symboli]
# print(Symbol0)
Position0 = csvdict['Position']
maxthreshold = float(max(csvdict['threshold']))
minthreshold = float(min(csvdict['threshold']))
# print(maxthreshold,minthreshold)

thismonth = classify_month(r'合约基本资料.xlsx', day_str_cm = '2022-03-10', col_ExpireDate_cm = '到期日', newcolED_cm = 'ExpireDays')
thismonth = Chg_col(thismonth, 
    oldcol = ['期权代码','认购/认沽','行权价'], 
    newcol = ['Symbol','CallOrPut','Strike'])
thismonth = thismonth[['Symbol','CallOrPut','Strike']]
# print(thismonth)

getmarketdata = GetData('username', 'password')
getmarketdata.ifind_api_login()

stockdata =  getmarketdata.get_stockprice_data(
    '510300.OF', 
    'tradeTime;preClose;latest')
stockprice = max(stockdata.latest)
callatm,putatm = selectATM(stockprice,thismonth,col_Symbol = 'Symbol',col_CallOrPut = 'CallOrPut', sign_CP = ['认购','认沽'], col_Strike = 'Strike')

data_greeks, stockprice = newdata(Symbol0,callatm,putatm)
# print(data_greeks)
Price0 = []
SymbolSH = []
for i in Symbol0:
    Price0.append(data_greeks.at[str(i)+'.SH','MidPrice'])
    SymbolSH.append(str(i)+'.SH')
dfold = initdata(Symbol = SymbolSH, Position = Position0, Price = Price0)
# print(dfold)

time_str = timecount()
fuseoption = Fuse()
loc = outputfile()
loc.exposition(dfold)

print(time_str)
while time_str < '15:00:00':
    time_str = timecount()

    stockdata =  getmarketdata.get_stockprice_data(
    '510300.OF', 
    'tradeTime;preClose;latest')
    stockprice = max(stockdata.latest)
    callatm,putatm = selectATM(stockprice,thismonth,col_Symbol = 'Symbol',col_CallOrPut = 'CallOrPut', sign_CP = ['认购','认沽'], col_Strike = 'Strike')
    AIO = select_optionAIO(thismonth, stockprice, 
        callorput_so = '认购', col_callorput_so = 'CallOrPut', 
        sign_CP = ['认购','认沽'], col_strike_so = 'Strike', col_code_so = 'Symbol' )
    AOTMcode = []
    AOTMcode.append(str(callatm))
    AOTMcode.append(str(AIO['OTM'][0]))
    AOTMcode.append(str(AIO['OTM'][1]))   
    # print(AOTMcode)
    
    dfold = loc.getexposi()
    oldsymbollist = dfold['newSymbol'].tolist()
    adjustlist = []
    for i in oldsymbollist:
        adjustlist.append(i[:-3])
    # print(adjustlist)
    Symbol0 += ['10004092'] + adjustlist + AOTMcode
    Symbol0 = list(set(Symbol0))
    # print(Symbol0)

    data_greeks, stockprice = newdata(Symbol0,callatm,putatm)

    fuseoption.clearhistorial()

    fuselist = fuseoption.getfuse(data_greeks, col_symbol_index = 'Symbol', col_sign = 'Fuse',fusesign = 'yes')
    # print (fuselist)

    ITMcode = ['10004092.SH']
    AOTMcodep = [x + '.SH' for x in AOTMcode]
    # print(AOTMcodep)
    # print (data_greeks)
    dfnew = netural_strategy(data_greeks, dfold, 
        ITMcodep = ITMcode, AOTMcodep = AOTMcodep, fuselist = fuselist,
        maxmarginp = 10000000.0, maxdeltap = maxthreshold, mindeltap = minthreshold)
    print (dfnew)


    tradingtime = time_str
    today = '20220310'
    stockprice = stockprice
    c = loc.calprofit(dfnew, dfold, stockprice = stockprice, tradingdate = today ,tradingtime = time_str)
    # print(c)
    # time.sleep(5)



