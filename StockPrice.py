import sys
import getopt

import tushare
import pandas
import numpy
import urllib
import urllib2
import os
import datetime

price_source='tushare' 

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
# tushare data version
def StockPrice_yahoo(stock, type, start, end):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=%s&ignore=.csv' % (stock, start.month-1, start.day, start.year, end.month-1, end.day, end.year, type)
    
    f=urllib2.urlopen(url, timeout=2)
    return pandas.read_csv(f, index_col=0).sort_index()

def StockPrice_tushare(stock, type, start, end):
    # maybe '300027.SZ' pattern, strip '.SZ' suffix
    stock=stock[0:6]

    if cmp(type, 'd')==0:
        data=tushare.get_h_data(stock, start.strftime('%Y-%m-%d'),
                                end.strftime('%Y-%m-%d'));
        
        data['Open']=data['open']
        data['High']=data['high']
        data['Close']=data['close']
        data['Low']=data['low']
        data['Adj Close']=data['close']
        data['Volume']=data['volume']
        return data.sort_index(ascending=True)
    elif cmp(type, 'w')==0:
        start_w = pandas.Timestamp(start - pandas.Timedelta(days=start.weekday())).normalize()
        end_w = pandas.Timestamp(end - pandas.Timedelta(days=end.weekday())+pandas.Timedelta(days=4)).normalize()
        if end_w > pandas.Timestamp.now():
            end_w = end_w - pandas.Timedelta(days=7)

        data=tushare.get_h_data(stock, start.strftime('%Y-%m-%d'),
                                end.strftime('%Y-%m-%d'));
        try:
            data=data.sort_index(ascending=True)
        except AttributeError, ex:
            data=tushare.get_hist_data(stock, start.strftime('%Y-%m-%d'),
                                       end.strftime('%Y-%m-%d'));
            data=data[['open','close','high','low','volume','price_change']]
            data=data.sort_index(ascending=True)            
        
        values=(end_w-start_w).days/7 + 1
        new_index=pandas.timedelta_range(start='4 days', periods=values, freq='7d')+start_w
        new_data=pandas.DataFrame(numpy.zeros(values*6).reshape(values, 6), index=new_index,columns=data.columns)

        for i in new_index:
            try:
                one_week_data=data.loc[i-pandas.Timedelta(days=4):i]
            except TypeError, ex:
                one_week_data=data.loc[(i-pandas.Timedelta(days=4)).strftime('%Y-%m-%d'):i.strftime('%Y-%m-%d')]

            if one_week_data['open'].count() == 0:
                if i == new_index[0]:
                    new_data.loc[i]=0
                    continue
                
#                new_data.loc[i]=new_data.loc[i-pandas.Timedelta(days=7)]
                new_data.loc[i]['open']=new_data.loc[i - pandas.Timedelta(days=7)]['close']
                new_data.loc[i]['close']=new_data.loc[i - pandas.Timedelta(days=7)]['close']
                new_data.loc[i]['high']=new_data.loc[i - pandas.Timedelta(days=7)]['close']
                new_data.loc[i]['low']=new_data.loc[i - pandas.Timedelta(days=7)]['close']
                new_data.loc[i]['volume']=0
                continue
            
            new_data.loc[i]['open']=one_week_data.iloc[0]['open']
            new_data.loc[i]['close']=one_week_data.iloc[one_week_data['close'].count()-1]['close']
            new_data.loc[i]['high']=one_week_data['high'].max()
            new_data.loc[i]['low']=one_week_data['low'].min()            
            new_data.loc[i]['volume']=one_week_data['volume'].sum()
            
        new_data['Open']=new_data['open']
        new_data['High']=new_data['high']
        new_data['Close']=new_data['close']
        new_data['Low']=new_data['low']
        new_data['Adj Close']=new_data['close']
        new_data['Volume']=new_data['volume']

        return new_data
    
    return Exception('Unsupported price type:%s' % type)
    
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

    # use price_source to choose real function
    return globals()['StockPrice_%s' % (price_source)](stock, type, start, end)
        
def StockPrice_2_fast(stock, type):
    url='http://real-chart.finance.yahoo.com/table.csv?s=%s&a=0&b=1&c=2015&d=11&e=11&f=2016&g=%s&ignore=.csv' % (stock, type)
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
    if cmp(type, 'w')==0: # need week price
        delta=datetime.timedelta(-end_dt.weekday())
        end_dt+=delta
    
    if cmp(start, end_dt.strftime('%Y-%m-%d')) == 0:
        return data

    try:
        new_data=StockPrice_4(stock, type, pandas.datetime.strptime(start, '%Y-%m-%d'), end_dt)
    except Exception, ex:
        return data

    # pandas.concat([datal, new_data[1:]]) emit wrong message
    new_data=new_data[1:]
    data=pandas.concat([data, new_data])

    # save to file using original order
    data.sort_index(ascending=False).to_csv(filename)
    
    return data

def StockPrice_2(stock, type):
    return StockPrice_4(stock ,type, '2015-01-01', pandas.datetime.now())

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

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)

        print argv[1], argv[2]
         
        print globals()[argv[1]](argv[2], argv[3], pandas.Timestamp(argv[4]), pandas.Timestamp(argv[5]))
    except Usage, err:
        print err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    
if __name__ == "__main__":
    sys.exit(main())
