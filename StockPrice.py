import tushare
import pandas
import urllib
import urllib2
import os

def StockPrice_old(stock):
    data=tushare.get_hist_data(stock, start='2015-01-01',end='2015-12-31')
    return data[['open','high','low','close','volume']].sort()

def StockPrice(stock):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2015&d=11&e=11&f=2016&g=d&ignore=.csv' % stock
    print url
    filename='%sd.csv' % stock
    print filename
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
        end_str=end
        end=pandas.datetime.strptime(end_str, '%Y-%m-%d')

    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=%s&ignore=.csv' % (stock, start.month-1, start.day, start.year, end.month-1, end.day, end.year, type)

    f=urllib2.urlopen(url)
    return pandas.read_csv(f, index_col=0).sort_index()

def StockPrice_w_3(stock, start, end):
    return StockPrice_4(stock, start, end, 'w')

def StockPrice_w_2(stock, start):
    return StockPrice_4(stock, start, pandas.datetime.now(), 'w')
    
def StockPrice_w(stock):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2015&d=11&e=11&f=2016&g=w&ignore=.csv' % stock
    filename='%sw.csv' % stock
    if not os.path.isfile(filename):
#        raise ValueError,'invalid argument'
        urllib.urlretrieve(url, filename)
    
    data=pandas.read_csv(filename, index_col=0).sort_index()
    start=data.index[data.index.size - 1]
    end_dt=pandas.datetime.now()
    if cmp(start, end_dt.strftime('%Y-%m-%d')) == 0:
        return data

    try:
        new_data=StockPrice_w_2(stock, pandas.datetime.strptime(start, '%Y-%m-%d'))
    except Exception, ex:
        return data

    # pandas.concat([datal, new_data[1:]]) emit wrong message
    new_data=new_data[1:]
    data=pandas.concat([data, new_data])

    # save to file using original order
    data.sort_index(ascending=False).to_csv(filename)
    
    return data
