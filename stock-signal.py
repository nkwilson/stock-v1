import tushare
import pandas

import StockPrice
import KDJ2
import RSI2
import ForceIndex2
import EMA

count=0

def KDJ_signal(hist_data):
    data=KDJ2.KDJ(hist_data,8)
    return 1 if data['J'][count-1] > data['J'][count-2] else 0

def RSI_signal(hist_data):
    data=RSI2.RSI(hist_data,13)
    return 1 if data['RSI'][count-1] > data['RSI'][count-2] else 0

def ForceIndex_signal(hist_data):
    data=ForceIndex2.FI(hist_data,13)
    return 1 if data['FI'][count-1] > data['FI'][count-2] else 0

def EMA_signal(hist_data):
    data=EMA.EMA(hist_data,13)
    return 1 if data['ema'][count-1] > data['ema'][count-2] else 0

def close_signal(hist_data):
    return 1 if hist_data['close'][count-1] > hist_data['close'][count-2] else 0

def adj_close_signal(hist_data):
    return 1 if hist_data['adj close'][count-1] > hist_data['adj close'][count-2] else 0

def calculate_stock_signal(hist_data):
    count=hist_data['Open'].count()
    
    if KDJ_signal(hist_data)*RSI_signal(hist_data)*ForceIndex_signal(hist_data) == 0:
        return 0
    else:
        return hist_data['Close'][count-1]


def stock_signal(stock):
    hist_data=StockPrice.StockPrice(stock)
    
    calculate_stock_signal(hist_data)

def stock_signal_w(stock):
    hist_data=StockPrice.StockPrice_w(stock)
    
    calculate_stock_signal(hist_data)
