import tushare
import pandas
import urllib
import os

def StockPrice(stock):
    data=tushare.get_hist_data(stock, start='2015-01-01',end='2015-12-31')
    return data[['open','high','low','close','volume']].sort()

def StockPrice_w(stock):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2015&d=11&e=11&f=2016&g=w&ignore=.csv' % stock
    filename='%sw.csv' % stock
    if not os.path.isfile(filename):
        urllib.urlretrieve(url, filename)
    data=pandas.read_csv(filename, index_col=0).sort_index()
    # for i in range(data.columns.values.size):
    #     data.columns.values[i]=data.columns.values[i].lower()
    return data

