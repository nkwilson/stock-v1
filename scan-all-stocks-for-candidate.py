# load stock-signal.py # load it by manual
# load load-code.py # load it by manual
import time
import random
import pandas

stocks=load_code_ex()
count=stocks[0].count()
data=pandas.DataFrame()
for i in range(count):
    try:
        ret=stock_signal_w_new_find_candidate(stocks[0][i])
        # df.insert(1, 'bar', df['one']) 插入一列
        # df['one_trunc'] = df['one'][:2] 
        if not isinstance(ret, type(None)) :
            ret.insert(0,'name', stocks[1][i])
            ret.insert(1,'code', stocks[0][i])
            pandas.concat([data, ret])
            print ret
    except ValueError, ve:
        continue
    except Exception, ex:
        print stocks[0][i],stocks[1][i],ex

data.to_csv('candidates.csv')
    
