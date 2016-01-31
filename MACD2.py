import numpy
import pandas
import EMA

EMA1_fast=12
EMA2_slow=26
DEA_period=9 #copied from tonghuashun's MACD setting

def MACD(hist_data, period):
    count=hist_data['Open'].count()
    data = pandas.DataFrame(numpy.zeros(count*6).reshape(count,6),
                            index=hist_data.index,
                            columns=['EMA1', 'EMA2', 'DIF', 'DEA', 'MACD', 'MACD_s'])
    
    data['EMA1']=EMA.EMA(hist_data, EMA1_fast)['EMA']
    data['EMA2']=EMA.EMA(hist_data, EMA2_slow)['EMA']

    data['DIF']=data['EMA1']-data['EMA2']

    #replace 'Adj Close' with 'DIF' to reuse EMA function
    hist_data['Adj Close']=data['DIF']
    data['DEA']=EMA.EMA(hist_data, DEA_period)['EMA']

    data['MACD']=2*(data['DIF']-data['DEA'])
    
    for i in range(count):
        data['MACD_s'][i]=1 if data['DIF'][i]>data['DIF'][i-1] else 0
    
    return data
