import LoadCode
import StockSignal

funds=LoadCode.load_etf_code()

ss_funds=[510010, 510050, 510210, 510290, 510500]
for i in ss_funds: StockSignal.stock_signal_w_new_find_candidate('%s.SS' % i)

sz_funds=[159915,159919, 159918, 159921, 159907, 159922]
for i in sz_funds: StockSignal.stock_signal_w_new_find_candidate('%s.SZ' % i)
    

