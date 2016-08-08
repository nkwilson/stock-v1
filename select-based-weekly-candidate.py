import sys
import getopt

import tushare
import pandas
import numpy
import os
import datetime

import StockPrice
import KDJ2
import RSI2
import ForceIndex2
import EMA

count=0
period=5

def select_base_weekly_candidate(file, date):
    print file, date
    
    data=pandas.read_csv(file)
    
    holding=data.select(lambda x: True if data.loc[x]['signal'] > 0 else False)

#    print holding[['Unnamed: 0', 'code', 'Volume', 'Adj Close', 'buy', 'name']].sort_values(['Volume'])
    
    selected=holding.select(lambda x: True if holding.loc[x]['Unnamed: 0'].find(date)==0 else False)

    print selected[['code', 'Volume', 'Adj Close', 'buy', 'name']].sort_values(['Volume'])


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

        print argv[1], argv[2], argv[3]
        
        print globals()[argv[1]](argv[2], argv[3])
    except Usage, err:
        print err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    
if __name__ == "__main__":
    sys.exit(main())
