# load stock-signal.py # load it by manual
# load load-code.py # load it by manual
import StockSignal
import LoadCode
import time
import random
import pandas

stocks=LoadCode.load_code_ex()
count=stocks[0].count()
data=pandas.DataFrame()
skip_before=''
skip=len(skip_before)
for i in range(count):
    try:
        if stocks[0][i].find(skip_before)==0:
            skip=0
        if skip > 0:
            continue;
        
        print stocks[0][i],stocks[1][i]
        ret=StockSignal.stock_signal_w_new_find_candidate(stocks[0][i])
        # df.insert(1, 'bar', df['one']) insert one column
        # df['one_trunc'] = df['one'][:2] 
        if not isinstance(ret, type(None)) :
            ret.insert(0,'name', stocks[1][i])
            ret.insert(1,'code', stocks[0][i])
            data=pandas.concat([data, ret])
            data.to_csv('candidates.csv')
            print ret
    except ValueError, ve:
        continue
    except Exception, ex:
        print stocks[0][i],ex
        time.sleep(random.random()*10)

if data.index.size > 0:
    data.sort_index().to_csv('candidates.csv')

    
