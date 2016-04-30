# -*- coding: utf-8 -*-

import StockSignal
import pandas

summary=None

stocks=[['600663.SS', '陆家嘴'],
        ['002673.SZ', '西部证券'],
        ['000973.SZ', '佛塑科技'],
        ['600030.SS', '中信证券'],
        ['002407.SZ', '多佛多'],
        ['002707.SZ', '众信旅游'],
        ['300359.SZ', '全通教育'],
        ['300431.SZ', '暴风科技'],
        ['002739.SZ', '万达院线'],
        ['300017.SZ', '网宿科技'],
        ['300027.SZ', '华谊兄弟'],
        ['300251.SZ', '光线传媒'],
        ['600633.SS', '浙报传媒'],
        ['002460.SZ', '赣锋锂业'],
        ['000938.SZ', '紫光股份'],
        ['300104.SZ', '乐视网']
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
