# -*- coding: utf-8 -*-

import StockSignal
import pandas

summary=None

stocks=[['002673.SZ', u'西部证券'],
          ['000973.SZ', '佛塑科技']]

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
    print summary.sort_index()
