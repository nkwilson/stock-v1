# -*- coding: utf-8 -*-

import StockSignal
import StockPrice
import pandas
import pp

funds=pandas.read_csv('fenji-funds.csv')

today=pandas.datetime.now().strftime('%Y-%m-%d')
summary=None
result_file='fenji-funds-candidates-%s.csv' % today

def local_func(stock, code, name):
    try:
        ret = StockSignal.stock_signal_w_new_find_candidate_with_volume(stock)

        ret.insert(0, 'code', code)
        ret.insert(ret.columns.size, 'name', name)

        return ret
    except Exception, ex:
        return None


ppservers = ()
jobs = []

job_server = pp.Server(12, ppservers=ppservers)

for i in range(funds['FundName'].count()):
    if funds['FundCode'][i] < 500000:
        stock='%s.SZ' % funds['FundCode'][i]
    else:
        stock='%s.SS' % funds['FundCode'][i]

    jobs.append(job_server.submit(local_func, (stock, funds['FundCode'][i], funds['FundName'][i]), (), ("StockSignal","pandas", )))


for job in jobs:
    ret = job()

    if isinstance(ret, type(None)):
        continue
    
    if not isinstance(summary, type(None)):
        summary=pandas.concat([ret, summary])
    else:
        summary=ret


if not isinstance(summary, type(None)):
    summary=summary.sort(['signal', 'Volume'])
#    summary=summary.sort_values(['code', 'Volume'])
    summary.to_csv(result_file)
    print summary.to_string();


    # sold=summary.select(lambda x: True if summary.loc[x]['signal']<0 else False)
    # hold=summary.select(lambda x: True if summary.loc[x]['signal']>0 else False)

    # # select those signaled today
    # sell_today=sold.select(lambda x: True if cmp(sold.loc[x][0], today)==0 else False)
    # buy_today=hold.select(lambda x: True if cmp(hold.loc[x][0], today)==0 else False)

    # sell_today.to_csv('sell-today-%s' % result_file)
    # buy_today.to_csv('buy-today-%s' % result_file)

    # print sell_today.to_string()
    # print buy_today.to_string()


    
