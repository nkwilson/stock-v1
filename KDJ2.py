import numpy
import pandas

def KDJ(hist_data, period):
    count=hist_data['Open'].count()
    data = pandas.DataFrame(numpy.zeros(count*7).reshape(count,7),
                            index=hist_data.index,
                            columns=['I','j','RSV','K','D','J','KDJ_s'])

    shift=0
    for i in range(count):
        if hist_data['Volume'][i] < 1:
            data['K'][i]=50
            shift=i
            continue;
        
        data['I'][i]=hist_data['Adj Close'][i] - hist_data['Low'][i-(period+shift):i].min()
        data['j'][i]=hist_data['High'][i-period:i].max() - hist_data['Low'][i-(period+shift):i].min()
        data['RSV'][i]=data['I'][i] / data['j'][i]*100
        
        if i < (period+shift):
            data['K'][i]=50
        else:
            data['K'][i]=2*data['K'][i-1]/3+data['RSV'][i]/3
        
        if i < (period+shift):
            data['D'][i]=50
        else:
            data['D'][i]=2*data['D'][i-1]/3+data['K'][i]/3
            data['J'][i]=3*data['K'][i]-2*data['D'][i]
        
        data['KDJ_s'][i]=1 if data['J'][i]>data['J'][i-1] else 0
    
    return data
