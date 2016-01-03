import numpy
import pandas

def EMA(hist_data, period):
    count=hist_data['Adj Close'].count()
    data = pandas.DataFrame(numpy.zeros(count).reshape(count,1),
                            index=hist_data.index,
                            columns=['ema'])

    for i in range(count):
        if i == period - 1:
            data['ema'][i]=hist_data['Adj Close'][0:i].sum()/period
        if i > (period-1):
            data['ema'][i]=(2*hist_data['Adj Close'][i]+(period-1)*data['ema'][i-1])/(period+1)
    return data


        
