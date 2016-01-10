# load stock-signal.py # load it by manual
# load load-code.py # load it by manual
import time
import random

stocks=load_code_ex()
count=stocks[0].count()
for i in range(count):
    try:
        ret=stock_signal_w_new_find_candidate(stocks[0][i])
        if not isinstance(ret, type(None)) :
            print stocks[1][i],ret
    except ValueError, ve:
        continue
    except Exception, ex:
        print stocks[0][i],stocks[1][i],ex
        time.sleep(random.randint(1,5))
        
    
