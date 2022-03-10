# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
import pandas as pd
import math
from math import log,sqrt,exp
from scipy import stats

class CalaulateGreeks:
    def __init__(self, stockprice,optionstrike,optionprice, timetoexpire,  callorput, riskfreerate,stockdividend): 
        self.s = stockprice
        self.k = optionstrike
        self.t = timetoexpire/365.0
        self.r = riskfreerate
        self.op = optionprice
        self.cp = callorput
        self.q = stockdividend
        self.st = sqrt(timetoexpire/365)
        self.ert = exp( - self.r * self.t)
        self.eqt = exp( - self.q * self.t)
    def bsm_call_value(self,sigma):
        d1 = ( math.log( self.s / self.k ) + ( self.r + 0.5 * sigma ** 2 ) * self.t )/( sigma * self.st )
        d2 = ( math.log( self.s / self.k ) + ( self.r - 0.5 * sigma ** 2 ) * self.t )/( sigma * self.st )
        sncd1 = stats.norm.cdf( d1, 0., 1.)
        sncd2 = stats.norm.cdf( d2, 0., 1.)
        callvalue = ( self.eqt * self.s * sncd1 - self.k * self.ert * sncd2)
        vega = self.s * sncd1 * self.st
        return callvalue, d1, d2, vega

    def bsm_put_value(self,sigma):
        d1 = ( math.log( self.s / self.k ) + ( self.r + 0.5 * sigma ** 2 ) * self.t )/( sigma * self.st )
        d2 = ( math.log( self.s / self.k ) + ( self.r - 0.5 * sigma ** 2 ) * self.t )/( sigma * self.st )
        sncd1 = stats.norm.cdf( -d1, 0., 1.)
        sncd2 = stats.norm.cdf( -d2, 0., 1.)
        putvalue = -( self.eqt * self.s * sncd1 - self.k * self.ert * sncd2)
        vega = self.s * sncd1 * self.st
        return putvalue, d1, d2, vega
    def bsm_call_imp_vol_newton(self, sigma_est = 1, iter = 1000):
        call_value = 1
        d1 = 1
        d2 = 1
        for i in range(iter):
            call_value, d1, d2, vega = CalaulateGreeks.bsm_call_value(self, sigma_est)
            if sigma_est < 10e-10:
                call_value, d1, d2, vega = CalaulateGreeks.bsm_call_value(self, 10e-10)
                return 10e-10, d1, d2
            sigma_est -= (( call_value - self.op) / vega)
        return sigma_est, d1, d2
    def bsm_put_imp_vol_newton(self, sigma_est = 1, iter = 1000):
        put_value = 1
        d1 = 1
        d2 = 1
        for i in range(iter):
            put_value, d1, d2, vega = CalaulateGreeks.bsm_put_value(self, sigma_est)
            sigma_est -= (( put_value - self.op) / vega)
        return sigma_est, d1, d2
    def call_greeks(self):
        sigma, d1, d2 = CalaulateGreeks.bsm_call_imp_vol_newton(self, sigma_est = 1, iter = 100)
        sncd1 = stats.norm.cdf( d1, 0., 1.)
        sncd2 = stats.norm.cdf( d2, 0., 1.)
        snpd1 = stats.norm.pdf( d1, 0., 1.)
        snpd2 = stats.norm.pdf( d2, 0., 1.)
        delta = self.eqt * sncd1
        deltacash = delta * self.s
        gamma = self.eqt * snpd1/(self.s * sigma * self.st)
        gammacash = gamma * 0.01 * self.s ** 2
        vega = self.eqt * self.s * self.st * snpd1
        theta = (((-self.s * snpd1 * sigma * self.eqt) / (2 * self.st) - self.r * self.k * self.ert * sncd2 + self.q * self.s * sncd1 * self.eqt))/252
        return sigma, delta, deltacash, gamma, gammacash, vega, theta
    def put_greeks(self):
        sigma, d1, d2 = CalaulateGreeks.bsm_put_imp_vol_newton(self, sigma_est = 1, iter = 100)
        sncd1 = stats.norm.cdf( d1, 0., 1.)
        sncd2 = stats.norm.cdf( d2, 0., 1.)
        sncd11 = stats.norm.cdf( -d1, 0., 1.)
        sncd22 = stats.norm.cdf( -d2, 0., 1.)
        snpd1 = stats.norm.pdf( d1, 0., 1.)
        snpd2 = stats.norm.pdf( d2, 0., 1.)
        delta = self.eqt * (sncd1-1.0)
        deltacash = delta * self.s 
        gamma = self.eqt * snpd1/(self.s * sigma * self.st)
        gammacash = gamma * 0.01 * self.s ** 2
        vega = self.eqt * self.s * self.st * snpd1
        theta = ((-self.s * snpd1 * sigma * self.eqt) / (2 * self.st) + self.r * self.k * self.ert * sncd22 - self.q * self.s * sncd11 * self.eqt)/252
        return sigma, delta, deltacash, gamma, gammacash, vega, theta


def get_greeks(df0_gg, synf_gg, riskfreerate_gg, stockdividend_gg, cpsign_gg = ['C','P'], listcol_gg = ['ExercisePrice','expireddays','CallOrPut','midPrice','ContractMultiplierUnit']):
    df_gg = df0_gg.copy()
    optionstrike_gg = df_gg['%s'%listcol_gg[0]].astype(float).tolist()
    timetoexpire_gg = df_gg['%s'%listcol_gg[1]].astype(float).tolist()
    callorput_gg = df_gg['%s'%listcol_gg[2]].tolist()
    optionprice_gg = df_gg['%s'%listcol_gg[3]].tolist()
    Multiplier = df_gg['%s'%listcol_gg[4]].astype(float).tolist()
    sigma_gg = []
    delta_gg = []
    deltacash_gg = []
    gamma_gg = []
    gammacash_gg = []
    vega_gg = []
    theta_gg = []
    csign_gg = cpsign_gg[0]
    psign_gg = cpsign_gg[1]
    for i in range(len(callorput_gg)):
        if callorput_gg[i] == csign_gg:
            contractgreeks_gg = CalaulateGreeks(synf_gg, optionstrike_gg[i], optionprice_gg[i], timetoexpire_gg[i], callorput_gg[i], riskfreerate_gg,stockdividend_gg)
            sigma1_gg, delta1_gg, deltacash0_gg, gamma1_gg, gammacash0_gg, vega1_gg, theta1_gg = contractgreeks_gg.call_greeks()
            deltacash1_gg = deltacash0_gg * Multiplier[i] 
            gammacash1_gg = gammacash0_gg * Multiplier[i] 
        elif callorput_gg[i] == psign_gg:
            contractgreeks_gg = CalaulateGreeks(synf_gg,optionstrike_gg[i],optionprice_gg[i], timetoexpire_gg[i], callorput_gg[i], riskfreerate_gg,stockdividend_gg)
            sigma1_gg, delta1_gg, deltacash0_gg, gamma1_gg, gammacash0_gg, vega1_gg, theta1_gg = contractgreeks_gg.put_greeks()
            deltacash1_gg = deltacash0_gg * Multiplier[i] 
            gammacash1_gg = gammacash0_gg * Multiplier[i] 
        else:
            print('getgreeks something wrong')
        sigma_gg.append(sigma1_gg)
        delta_gg.append(delta1_gg)
        deltacash_gg.append(deltacash1_gg)
        gamma_gg.append(gamma1_gg)
        gammacash_gg.append(gammacash1_gg)
        vega_gg.append(vega1_gg)
        theta_gg.append(theta1_gg)
    df_gg['Sigma'] = sigma_gg
    df_gg['Delta'] = delta_gg
    df_gg['Deltacash'] = deltacash_gg
    df_gg['Gamma'] = gamma_gg
    df_gg['Gammacash'] = gammacash_gg
    df_gg['Vega'] = vega_gg
    df_gg['Theta'] = theta_gg
    return df_gg



    

