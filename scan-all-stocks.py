# load stock-signal.py # load it by manual
# load load-code.py # load it by manual
import time

stocks=load_code_ex()

for i in range(stocks[0].count()):
    try:
        stock_signal_w_new(stocks[0][i])
        time.sleep(1)
    except Exception, ex:
        print ex

    
