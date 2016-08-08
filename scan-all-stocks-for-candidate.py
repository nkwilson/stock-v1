# load stock-signal.py # load it by manual
# load load-code.py # load it by manual
import StockSignal
import LoadCode
import time
import random
import pandas
import pp

stocks=LoadCode.load_code_ex()
count=stocks[0].count()
data=pandas.DataFrame()
skip_before=''
skip=len(skip_before)
summary=None
result_file='candidates-%s.csv' % pandas.datetime.now().strftime('%Y-%m-%d')


def local_func(stock, code, name):
    try:
        ret = StockSignal.stock_signal_w_new_find_candidate_with_volume(stock)

        if not isinstance(ret, type(None)):
            # df.insert(1, 'bar', df['one']) insert one column
            # df['one_trunc'] = df['one'][:2] 
            ret.insert(0, 'code', code)
            ret.insert(ret.columns.size, 'name', name)

        return ret
    except Exception, ex:
        return None

ppservers = ()
jobs = []

start_time = time.time()

# Total cpus=4, 8 performance the best among [4,8,12,16,24]
job_server = pp.Server(8, ppservers=ppservers)

for i in range(count):
    if stocks[0][i].find(skip_before)==0:
        skip=0
    if skip > 0:
        continue;
        
    jobs.append(job_server.submit(local_func, (stocks[0][i], stocks[0][i], stocks[1][i]), (), ("StockSignal", "pandas", )))

for job in jobs:
    ret = job()

    if isinstance(ret, type(None)):
        continue

    if not isinstance(summary, type(None)):
        summary=pandas.concat([ret, summary])
    else:
        summary=ret

print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()
        
if not isinstance(summary, type(None)):
    summary=summary.sort(['profit'])
    summary.to_csv(result_file)

    print summary[['code', 'signal', 'Volume', 'buy', 'sell', 'profit', 'name']].sort_values(['signal'])

    # # select those have been sold
    # sold=summary2.select(lambda x: True if summary2.loc[x]['signal']==-1 else False)
    # holding=summary2.select(lambda x: True if summary2.loc[x]['signal']==1 else False)
    
    # print sold.to_string()
    # print holding.to_string()
