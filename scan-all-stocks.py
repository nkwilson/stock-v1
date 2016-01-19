# load stock-signal.py # load it by manual
# load load-code.py # load it by manual
import StockSignal
import LoadCode
import time
import random

stocks=LoadCode.load_code_ex()
count=stocks[0].count()
left=count
loop=0
while left > 0:
    count=left
    print '##### loop %d begin ####' % loop
    loop=loop+1
    for i in range(count):
        try:
            print stocks[1][i],StockSignal.stock_signal_w_new_simple(stocks[0][i])
            left=left-1
        except ValueError, ve:
            left=left-1
            continue
        except Exception, ex:
            print stocks[0][i],stocks[1][i],ex
            time.sleep(random.randint(1,5))

    
