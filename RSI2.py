import numpy
import pandas

def RSI(hist_data, period):
    count = hist_data['Open'].count()
    data = pandas.DataFrame(numpy.zeros(count*4).reshape(count,4),
                            index=hist_data.index,
                            columns=['X','A','B','RSI'])

    for i in range(count):
        data['X'][i]=hist_data['Adj Close'][i] - hist_data['Adj Close'][i-1]

        if i > (period-1):
            data['A'][i]=data['X'][i-period:i].apply(lambda x: x if x > 0 else 0).sum()
            data['B'][i]=data['X'][i-period:i].apply(lambda x: x if x < 0 else 0).sum()
            data['RSI'][i]=data['A'][i]/(data['A'][i]-data['B'][i]) *100

    
    return data


        
