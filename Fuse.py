# -*- coding: utf-8 -*-
'''
@author: Zhuojinjun
'''
class Fuse():
    def __init__(self):
        globals()['fuse'] = []
    def getfuselist(self):
        return globals()['fuse']
    def addfusecontract(self, contract):
        globals()['fuse'].append(contract)
    def getfuse(self, fusedf, col_symbol_index = 'Symbol', col_sign = 'Fuse',fusesign = 'yes'):
        fusesymbol = fusedf[col_symbol_index].tolist()
        fuse = fusedf[col_sign].tolist()
        k = len(fusesymbol)
        for i in range(k):
            if fuse[i] == fusesign:
                Fuse.addfusecontract(self,fusesymbol[i])
            else:
                pass
        return globals()['fuse']
    def clearhistorial(self):
        globals()['fuse']=[]

    def dropfusecontract(self,hedgecode,fuselist):
        newhedgecode = []
        for i in hedgecode:
            if i in fuselist:
                pass
            else:
                newhedgecode.append(i)
        return newhedgecode
