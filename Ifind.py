'''
@author: Zhuojinjun
'''
from iFinDPy import *

class GetData:
    def __init__(self, username, password ):
        self.username = username
        self.password = password
    def ifind_api_login(self):
        thsLogin = THS_iFinDLogin(self.username,self.password)
    def ifind_api_logout(self):
        thsLogout = THS_iFinDLogout()
    def get_option_data(self, codelist, attributes):
        return THS_RQ(codelist, attributes).data
    def get_stockprice_data(self, codelist, attributes):
        return THS_RQ(codelist, attributes).data
    def get_option_data_BD(self, codelist, attributes1, attributes2):
        return THS_BD(codelist, attributes1,attributes2).data
