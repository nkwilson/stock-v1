import LoadCode
import StockSignal
import StockPrice
import pandas
import pp

funds=LoadCode.load_etf_code()

summary=None
result_file='funds-candidates-%s.csv' % pandas.datetime.now().strftime('%Y-%m-%d')

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

    print ret
    
    if not isinstance(summary, type(None)):
        summary=pandas.concat([ret, summary])
    else:
        summary=ret


if not isinstance(summary, type(None)):
    summary=summary.sort(['Volume'])
#    summary=summary.sort_values(['code', 'Volume'])
    summary.to_csv(result_file)
    print summary.to_string();
