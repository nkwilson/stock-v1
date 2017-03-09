# -*- coding: utf-8 -*-
import sys
import getopt

import pandas
import numpy
import StockSignal
import pp
import datetime

#data=pandas.read_csv('600663.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('600547.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('000002.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('000333.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('000651.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('000799.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('000938.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('002407.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('002460.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('002587.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('002673.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('600519.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('600799.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('300017.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('300027.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('300104.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('300251.SZw-all-data.csv', index_col=0).sort_index()

#data=pandas.read_csv('510050.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('510300.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('510500.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('511010.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('518800.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('510900.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('159920.SZw-all-data.csv', index_col=0).sort_index()

#data=pandas.read_csv('150206.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('150153.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('150195.SZw-all-data.csv', index_col=0).sort_index()

# copied from scan-these-stocks.py
stocks=[
#        ['600663', '陆家嘴', '2016-12-01', ''],
#	['000651', '格力电器', '2016-12-01', ''],
#	['601668', '中国建筑', '2016-12-01', ''],
#        ['002673', '西部证券', '2016-12-01', ''],
#        ['300017', '网宿科技', '2016-12-01', ''],
#	['300104', '乐视网', '2016-12-01', ''],
#        ['300027', '华谊兄弟', '2016-12-01', ''],
#        ['300251', '光线传媒', '2016-12-01', ''],
#        ['000938', '紫光股份', '2016-12-01', ''],
#        ['600839', '四川长虹', '2016-12-01', ''],
#        ['002308', '威创股份', '2016-12-01', ''], # 幼儿教育产业
#        ['002638', '勤上光电', '2016-12-01', ''],
#	['000002', '万科A', '2016-12-01', ''],
#        ['511010',  '国债ETF', '2016-12-01', ''],
#        ['600547', '山东黄金', '2016-11-01', ''],
#        ['000333', '美的集团', '2016-09-01', ''],
#        ['002407', '多佛多', '2016-01-01', ''],
#        ['002460', '赣锋锂业', '2016-01-01', ''],
#        ['000799', '酒鬼酒', '2016-09-01', ''],
#        ['600519', '贵州茅台', '2016-09-01', ''],
#        ['600779', '水井坊', '2016-09-01', ''],
#        ['600887', '伊利股份', '2016-09-01', ''],
#        ['300160', '秀强股份', '2016-09-01', ''],
        ['510050',  '50ETF', '2016-01-01', ''],
        ['510300',  '300ETF', '2016-01-01', ''],
        ['510500',  '500ETF', '2016-01-01', ''],
#        ['518800', '黄金基金', '2016-01-01', ''],
#        ['159920', '恒生ETF', '2016-09-01', ''],
#        ['510900', 'H股ETF', '2016-09-01', ''],
        ['159915', '创业板', '2016-01-01', ''],
#        ['159902', '中小板', '2016-09-01', ''],
#        ['150023', '深成指B', '2016-09-01', ''],
#        ['150201', '券商B', '2016-09-01', ''],
#        ['150153', '创业板B', '2016-09-01', ''],
]

def new_weekly_policy (data):
        # global next_buy, selling_good_deals, next_half_buy, next_steady_buy
        # global global_tendency, lodgers, total_op_count, total_cost
        # global deal_cost, total_money, do_half_buy, do_steady_buy
        # global show_detail, show_signal, show_summary, show_verbose
        
        lodgers=None
        
        only_lastest_weeks = 5000 # lastest 50 weeks
        selling_good_deals=-1
        with_profit=0.06
        force_selling_good_deals=-1 # if total_cost is reach, then sell profit more than 10%
        forced_with_profit=0.6
        next_buy=-1
        next_half_buy=-1  # buy half cost when globa_tendency=1 and close_s=1
        next_steady_buy=-1 # buy one cost 
        global_tendency=0
        deal_cost=37000
        deal_count=12  # at most this many deals
        total_money=deal_count * deal_cost # all of my money
        total_cost=0 # total cost of holding until now, must be less than total_money
        current_profit=0 
        do_half_buy=0
        do_steady_buy=1
        show_detail=1
        show_signal=1
        show_summary=1
        total_op_count=0
        show_verbose=0
        profit_invested=1  # using profit to buy more stocks
        profit_multi=3 # must left that much as cash
        count = data['signal'].count()
        # if no volume, return now
        if data['Volume'][count-1] == 0:
                return
        for i in range(count):
            if show_verbose > 0 :
                print '### round %d' % i 
                print data.iloc[i][['Open', 'Volume']] 
            if data['Volume'][i] == 0:
                continue
            if selling_good_deals == 0 and force_selling_good_deals == 0 and next_buy==0 and next_half_buy==0 and next_steady_buy == 0:
                print "*** Empty round %d" % i
                continue
            if (selling_good_deals > 0 or force_selling_good_deals > 0) and not isinstance(lodgers, type(None)):
                # find those holding deals, sell-price is empty
               deals=lodgers.select(lambda x: True if lodgers.loc[x]['sell-price'] == 0 else False)
               if selling_good_deals > 0:
                       to_sold_deals=deals.select(lambda x: True if deals.loc[x]['price']*(1+with_profit) < data['Open'][i] else False)
               else:
                       to_sold_deals=deals.select(lambda x: True if deals.loc[x]['price']*(1+forced_with_profit) < data['Open'][i] else False)                       
               if isinstance(to_sold_deals, type(None)):
                   continue;
               if show_verbose > 0:
                if to_sold_deals['price'].count() == 0:
                  print "Nothing to sold"
                else:
                  print to_sold_deals[['price','count','total']]
               for j in range(to_sold_deals['price'].count()):
                   #           print data.index[i]
                   lodgers.loc[to_sold_deals.index[j]]['sell-date']=data.index[i]
                   lodgers.loc[to_sold_deals.index[j]]['sell-price']=data['Open'][i]
                   lodgers.loc[to_sold_deals.index[j]]['profit']=(data['Open'][i]-to_sold_deals['price'][j])*to_sold_deals['count'][j]
                   total_cost -= lodgers.loc[to_sold_deals.index[j]]['total']
                   current_profit += lodgers.loc[to_sold_deals.index[j]]['profit']
                   # if with big profit, increase total_money
                   if current_profit > profit_multi * deal_cost and profit_invested == 1:
                     total_money += deal_cost
                     current_profit-= deal_cost
                   if show_verbose > 0:
                     print total_money, current_profit
               if show_verbose > 0 :
                print lodgers[['price','count','total','sell-date','sell-price']] 
            selling_good_deals=-1
            force_selling_good_deals=-1
            if next_buy > 0 or next_half_buy > 0 or next_steady_buy > 0:
                new_row_data=pandas.DataFrame(index=data.index[i:i+1], columns=['price', 'count', 'total', 'total-cost', 'sell-date', 'sell-price', 'profit'])
                new_row_data['price'][0]=data['Open'][i]
                count=int(deal_cost / data['Open'][i]/100.0) * 100
                if next_half_buy > 0 and count >= 200:
                    count=count / 2
                new_row_data['count'][0]=count
                new_row_data['total'][0]=new_row_data['count'][0] * data['Open'][i]
                #        new_row_data['signal'][0]=0
                #        new_row_data['close_s'][0]=0
                new_row_data['sell-date'][0]=data.index[i]
                new_row_data['sell-price'][0]=0
                new_row_data['profit'][0]=0        
                total_cost += new_row_data['total'][0]
                new_row_data['total-cost'][0]=total_cost
                if isinstance(lodgers, type(None)):
                    lodgers=new_row_data
                else:
                    lodgers=lodgers.append(new_row_data)
                    #        print lodgers
            next_buy=-1
            next_half_buy=-1
            next_steady_buy=-1
            if show_verbose > 0 :
                print 'signal %d close_s %d EMA_s %d global %d' % (data['signal'][i], data['close_s'][i], data['EMA_s'][i], global_tendency) 
            if data['signal'][i] < 0:
                selling_good_deals=1
            elif data['signal'][i] > 0 and (total_money - total_cost) > deal_cost:
                next_buy=1
            else :
                if global_tendency < 1:
                        selling_good_deals=1
                if (total_money - total_cost) > deal_cost:
                        if data['close_s'][i] == 0:
                                next_buy=1
                        elif do_half_buy > 0:
                                next_half_buy=1
                        elif do_steady_buy > 0:
                                next_steady_buy=1
                elif selling_good_deals < 1:
                        force_selling_good_deals=1
            global_tendency = data['EMA_s'][i]
            if show_verbose > 0:
                print 'selling %d force_selling %d next_buy %d next_half_buy %d global %d' % (selling_good_deals,
                                                                                              force_selling_good_deals, 
                                                                                        next_buy, next_half_buy, global_tendency)
        # generate signal for next operation, buy and/or sell?
        if show_signal > 0 and not isinstance(lodgers, type(None)):
            last=data['Open'].count()-1
            price=data.iloc[last]['Open']
            sellings=lodgers.select(lambda x: True if (lodgers.loc[x]['sell-date'] == data.index[last] and lodgers.loc[x]['sell-price'] > 0)
                                                   else False)['count']
            #    print sellings
            if (sellings.count() > 0):
                    total_op_count -= sellings.sum()

            # sellings=lodgers.select(lambda x: True if (lodgers.loc[x]['price'] < price and lodgers.loc[x]['sell-price'] == 0)
            #                                        else False)['count']
            # if (sellings.count() > 0):
            #         total_op_count -= sellings.sum()
        if (next_buy > 0 or next_half_buy > 0 or next_steady_buy > 0) and show_signal > 0:
            last=data['Open'].count()-1
            count=int(deal_cost / data.iloc[last]['Open']/100.0) * 100
            if next_half_buy > 0 and count >= 200:
                count=count / 2
            if count > 0 and total_op_count == 0:
                print '+%d' % count
        if (total_op_count != 0):
                print '%d' % total_op_count
        if show_summary > 0:
            last=data['Open'].count()-1
            price=data.iloc[last]['Open']
            holdings=lodgers.select(lambda x: True if lodgers.loc[x]['sell-price']==0 else False)
            total_profit=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['profit'].sum()
            total_profit2=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['profit']/lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['total']
            total_flows=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['total'].sum()
            if total_flows > 0:
                    print '### flows %d profit %d rate %.3f rate2 %.3f holding %d(=%d) pending %d left %d' % (total_flows, total_profit, total_profit/total_flows, total_profit2.sum() / total_profit2.count(),
                                                                                                              holdings['count'].sum(),
                                                                                                              holdings['total'].sum(),
                                                                                                              holdings['count'].sum() * price - holdings['total'].sum(),
                                                                                                              total_money-total_cost+current_profit)
        if show_detail > 0:
            print lodgers
ppservers = ()
jobs = []

job_server = pp.Server(ppservers=ppservers)

def local_func1(stock, start, end):
        StockSignal.stock_signal_w_new_find_candidate(stock, start, end)

def local_func_d(stock, start, end):
        StockSignal.stock_signal_d_new_find_candidate(stock, start, end)

def one_stock(stock, start, end):
        local_func1(stock, start, end)
        data = pandas.read_csv('%sw-all-data.csv' % stock, index_col=0).sort_index()

        print stock
        new_weekly_policy(data)

def one_stock_d(stock, start, end):
        local_func_d(stock, start, end)
        data = pandas.read_csv('%sd-all-data.csv' % stock, index_col=0).sort_index()

        print stock
        new_weekly_policy(data)
        
def __main():
        for s in stocks:
                jobs.append(job_server.submit(local_func1, (s[0], s[2], s[3]), (), ("StockSignal", "pandas", )))

        job_server.wait()
        print ''
        
        #use pp for following computing is not so good
        for s in stocks:
                data=pandas.read_csv('%sw-all-data.csv' % s[0], index_col=0).sort_index()

                print s[1]
                new_weekly_policy(data)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

#pandas.read_csv('510300w-all-data.csv', index_col=0)[['EMA', 'signal']][-60:].plot(kind='bar',figsize=(20,12),title='ETF300').figure.show()
#figure.savefig('a.svg', format='svg')

def main(argv):
    print argv

    if len(argv) == 1:
        __main()
        return

    # 2 args: one_stock ######, last year
    if len(argv) == 3:
            end = pandas.datetime.now();
            start=end-datetime.timedelta(365)
            
            globals()[argv[1]](argv[2],start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    # 3 args: one_stock ######, start, until now
    elif len(argv) == 4:
            globals()[argv[1]](argv[2], argv[3], pandas.datetime.now().strftime('%Y-%m-%d'))
    elif len(argv) == 5:
    # 4 args: one_stock ######, start, end
            globals()[argv[1]](argv[2], argv[3], argv[4])
    else:
            print "Usage: program [one_stock [stock [start [end]]]]"

if __name__ == "__main__":
        sys.exit(main(sys.argv))

        
        


