import tushare
import pandas
import urllib
import urllib2
import os
import datetime

def StockPrice_old(stock):
    data=tushare.get_hist_data(stock, start='2015-01-01',end='2015-12-31')
    return data[['open','high','low','close','volume']].sort()

def StockPrice(stock):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2015&d=11&e=11&f=2016&g=d&ignore=.csv' % stock
    filename='%sd.csv' % stock
    if not os.path.isfile(filename):
        urllib.urlretrieve(url, filename)
    data=pandas.read_csv(filename, index_col=0).sort_index()
    # for i in range(data.columns.values.size):
    #     data.columns.values[i]=data.columns.values[i].lower()
    return data

def StockPrice_4(stock, type, start, end):
    if isinstance(start, str):
        start_str=start
        start=pandas.datetime.strptime(start_str, '%Y-%m-%d')
    elif isinstance(start, datetime.datetime):
        start_str=start.strftime('%Y-%m-%d')
    else:
        raise Exception('StockPrice_4 start')
    
    if isinstance(end, str):
        end_str=end
        end=pandas.datetime.strptime(end_str, '%Y-%m-%d')
    elif isinstance(end, datetime.datetime):
        end_str=end.strftime('%Y-%m-%d')
    else:
        raise Exception('StockPrice_4 end')            

    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=%s&ignore=.csv' % (stock, start.month-1, start.day, start.year, end.month-1, end.day, end.year, type)
    
    f=urllib2.urlopen(url, timeout=2)
    return pandas.read_csv(f, index_col=0).sort_index()
    
def StockPrice_2(stock, type):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2008&d=11&e=11&f=2016&g=%s&ignore=.csv' % (stock, type)
    filename='%s%s.csv' % (stock, type)
    if not os.path.isfile(filename):
#        raise ValueError,'invalid argument'
        f=urllib2.urlopen(url, timeout=2)
        data=pandas.read_csv(f, index_col=0)
        data.to_csv(filename)
    else:
        data=pandas.read_csv(filename, index_col=0)
        
    data=data.sort_index()        
    start=data.index[data.index.size - 1]
    end_dt=pandas.datetime.now()
    if cmp(start, end_dt.strftime('%Y-%m-%d')) == 0:
        return data

    try:
        new_data=StockPrice_4(stock, type, pandas.datetime.strptime(start, '%Y-%m-%d'), pandas.datetime.now())
    except Exception, ex:
        return data

    # pandas.concat([datal, new_data[1:]]) emit wrong message
    new_data=new_data[1:]
    data=pandas.concat([data, new_data])

    # save to file using original order
    data.sort_index(ascending=False).to_csv(filename)
    
    return data

def StockPrice_w_3(stock, start, end):
    return StockPrice_4(stock, 'w', start, end)

def StockPrice_w_2(stock, start):
    return StockPrice_4(stock, 'w', start, pandas.datetime.now())

def StockPrice_w(stock):
    return StockPrice_2(stock, 'w')

def StockPrice_d_3(stock, start, end):
    return StockPrice_4(stock, 'd', start, end)

def StockPrice_d_2(stock, start):
    return StockPrice_4(stock, 'd', start, pandas.datetime.now())
    
def StockPrice_d(stock):
    return StockPrice_2(stock, 'd')
