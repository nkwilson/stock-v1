# load stock-signal.py # load it by manual
# load load-code.py # load it by manual
import time
import random

stocks=load_code_ex()

for i in range(stocks[0].count()):
    try:
        stock_signal_w_new(stocks[0][i])
    except ValueError, ve:
        continue
    except Exception, ex:
        print stocks[0][i],stocks[1][i],ex
        time.sleep(random.randint(1,5))

    
