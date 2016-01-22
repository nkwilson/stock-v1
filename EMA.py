import numpy
import pandas

def EMA(hist_data, period):
    count=hist_data['Adj Close'].count()
    data = pandas.DataFrame(numpy.zeros(count*2).reshape(count,2),
                            index=hist_data.index,
                            columns=['EMA','EMA_s'])

    for i in range(count):
        if hist_data['Volume'][i] < 1:
            data['EMA'][i]=hist_data['Adj Close'][i]
            continue;
        
        if i == period - 1:
            data['EMA'][i]=hist_data['Adj Close'][0:i].sum()/period
        if i >= period:
            data['EMA'][i]=(2*hist_data['Adj Close'][i]+(period-1)*data['EMA'][i-1])/(period+1)
        data['EMA_s'][i]=1 if data['EMA'][i]>data['EMA'][i-1] else 0
    
    return data


        
