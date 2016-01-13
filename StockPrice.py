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

def StockPrice_w_3(stock, start, type):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=11&e=11&f=2016&g=%s&ignore=.csv' % (stock, start.month-1, start.day, start.year, type)
    f=urllib2.urlopen(url)
    return pandas.read_csv(f, index_col=0).sort_index()
    
def StockPrice_w(stock):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2015&d=11&e=11&f=2016&g=w&ignore=.csv' % stock
    filename='%sw.csv' % stock
    if not os.path.isfile(filename):
#        raise ValueError,'invalid argument'
        urllib.urlretrieve(url, filename)
    
    data=pandas.read_csv(filename, index_col=0).sort_index()
    start=data.index[data.index.size - 1]
    if cmp(start, pandas.datetime.now().strftime('%Y-%M-%d')) == 0:
        return data

    try:
        new_data=StockPrice_w_3(stock, pandas.datetime.strptime(start, '%Y-%M-%d'), 'w')
    except Exception, ex:
        print ex
        return data

    # pandas.concat([data, new_data[1:]]) emit wrong message
    new_data=new_data[1:]
    data=pandas.concat([data, new_data])

    data.sort_index(ascending=False).to_csv(filename)
    
    return data
