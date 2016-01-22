import numpy
import pandas

def RSI(hist_data, period):
    count = hist_data['Open'].count()
    data = pandas.DataFrame(numpy.zeros(count*5).reshape(count,5),
                            index=hist_data.index,
                            columns=['X','A','B','RSI','RSI_s'])

    for i in range(count):
        if hist_data['Volume'][i] < 1:
            continue;
        
        data['X'][i]=hist_data['Adj Close'][i] - hist_data['Adj Close'][i-1]

        if i >= period:
            data['A'][i]=data['X'][i-period:i].apply(lambda x: x if x > 0 else 0).sum()
            data['B'][i]=data['X'][i-period:i].apply(lambda x: x if x < 0 else 0).sum()
            data['RSI'][i]=data['A'][i]/(data['A'][i]-data['B'][i]) *100

        data['RSI_s'][i]= 1 if data['RSI'][i]>data['RSI'][i-1] else 0
    
    return data


        
