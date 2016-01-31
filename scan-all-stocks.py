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
            sum=StockSignal.stock_signal_w_new_sum(stocks[0][i])
            if sum > 2.0:
                print stocks[1][i],stocks[0][i],sum
            left=left-1
        except ValueError, ve:
            left=left-1
            continue
        except Exception, ex:
            print ex

    
