import numpy
import pandas

def FI(hist_data, period):
    count = hist_data['Open'].count()
    data = pandas.DataFrame(numpy.zeros(count*2).reshape(count,2),
                            index=hist_data.index,
                            columns=['F','FI'])

    for i in range(count):
        data['F'][i]=(hist_data['Adj Close'][i] - hist_data['Adj Close'][i-1])*hist_data['Low'][i]

        if i > period:
            data['FI'][i]=(data['F'][i]*2 + data['F'][i-1]*(period-1))/(period+1)
    return data
