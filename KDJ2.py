import numpy
import pandas

def KDJ(hist_data, period):
    count=hist_data['Open'].count()
    data = pandas.DataFrame(numpy.zeros(count*6).reshape(count,6),
                            index=hist_data.index,
                            columns=['I','j','RSV','K','D','J'])

    for i in range(count):
        data['I'][i]=hist_data['Adj Close'][i] - hist_data['Low'][i-period:i].min()
        data['j'][i]=hist_data['High'][i-period:i].max() - hist_data['Low'][i-period:i].min()
        data['RSV'][i]=data['I'][i] / data['j'][i]*100
        if i < (period+1):
            data['K'][i]=50
        else:
            data['K'][i]=2*data['K'][i-1]/3+data['RSV'][i]/3
        if i < (period+1):
            data['D'][i]=50
        else:
            data['D'][i]=2*data['D'][i-1]/3+data['K'][i]/3
            data['J'][i]=3*data['K'][i]-2*data['D'][i]

    return data


        
