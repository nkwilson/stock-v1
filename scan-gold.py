# -*- coding: utf-8 -*-

import StockSignal
import pandas

summary=None

stocks=[['002155.SZ', '湖南黄金'],
        ['002237.SZ', '恒邦股份'],
        ['600547.SS', '山东黄金'],
        ['600489.SS', '中金黄金'],
        ['601069.SS', '西部黄金'],
        ['600311.SS', '荣华实业'],
        ['600988.SS', '赤峰黄金'],
        ['600766.SS', '园成黄金'],
        ['600146.SS', '商赢环球'],
        ['600687.SS', '刚泰控股'],
        ['601899.SS', '紫金矿业'],
        ['000506.SZ', '中润资源'],
]

for i in stocks:
    try:
        ret = StockSignal.stock_signal_w_new_find_candidate(i[0])
    except Exception, ex:
        ret = None

    if not isinstance(ret, type(None)) :
        ret.insert(0,'name', i[1])
        ret.insert(1,'code', i[0])
        
        if not isinstance(summary, type(None)):
#            summary=pandas.DataFrame.append(summary,ret)
            summary=pandas.concat([ret, summary])
        else:
            summary=ret

if not isinstance(summary, type(None)):            
    print summary[['code','signal', 'buy', 'sell','profit','name']].sort_values(['signal'])
