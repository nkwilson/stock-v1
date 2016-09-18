# -*- coding: utf-8 -*-

import StockSignal
import pandas

summary=None

stocks=[['600663.SS', '陆家嘴'],
        ['000333.SZ', '美的集团'],
        ['002673.SZ', '西部证券'],
        ['002407.SZ', '多佛多'],
        ['002460.SZ', '赣锋锂业'],
        ['300017.SZ', '网宿科技'],
        ['300027.SZ', '华谊兄弟'],
        ['300251.SZ', '光线传媒'],
        ['000938.SZ', '紫光股份'],
        ['600547.SS', '山东黄金'],
        ['000799.SZ', '酒鬼酒'],
        ['600519.SS', '贵州茅台'],
        ['600779.SS', '水井坊'],
	['000002.SZ', '万科A'],
	['300104.SZ', '乐视网'],
	['000651.SZ', '格力电器'],
        ['600887.SS', '伊利股份'],
]

for i in stocks:
    try:
        ret = StockSignal.stock_signal_w_new_find_candidate(i[0])
    except Exception, ex:
        print i[1]
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
    result=summary[['code','signal', 'buy', 'sell','profit','name']].sort_values(['signal'])
    result.to_csv('scan-these-stocks-candidates-%s.csv' % pandas.datetime.now().strftime('%Y-%m-%d'))
    print '\n',result

