#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt

import pandas
import numpy
import StockSignal
import pp
import datetime
import tushare

import os.path as path
import time

import matplotlib as mpl

import matplotlib.pyplot as pyplot


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
        # code, name, start, end, budget, deal-count, first-buy  #, more-budget
	['000002', '万科A', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600521', '华海药业', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600276', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600887', '伊利股份', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600487', '亨通光电', '2014-01-01', '', 100000, 8, '2017-01-01'],
#        ['600240', '华电资本', '2014-01-01', '', 0, 0, ''],
#        ['601669', '中国电建', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600660', '福耀玻璃', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600519', '贵州茅台', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000858', '五粮液', '2014-01-01', '', 100000, 8, '2017-01-01'],        
#        ['300017', '网宿科技', '2014-01-01', '', 0, 0, ''],
#        ['002407', '多佛多', '2014-01-01', '', 0, 0, ''],
        ['002460', '赣锋锂业', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000651', '格力电器', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000333', '美的集团', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002508', '老板电器', '2014-01-01', '', 100000, 8, '2017-01-01'],        
        ['002415', '海康威视', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['601318', '中国平安', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600298', '安琪酵母', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600036', '招商银行', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['300176', '鸿特精密', '2014-01-01', '', 100000, 8, '2017-01-01'],
#        ['510050',  '50ETF', '2014-01-01', '', 100000, 8, '2017-01-01'],
#        ['510300',  '300ETF', '2014-01-01', '', 0, 0, ''],
#        ['510500',  '500ETF', '2014-01-01', '', 100000, 8, '2017-07-01'],
#        ['159915', '创业板', '2014-01-01', '', 100000, 8, '2017-07-01'],
#        ['150201', '券商B', '2014-01-01', '', 0, 0, ''],
#        ['150153', '创业板B', '2014-01-01', '', 0, 0, ''],
#        ['159902', '中小板', '2016-09-01', '', 0, 0, ''],
#        ['150023', '深成指B', '2016-09-01', '', 0, 0, ''],
#        ['518800', '黄金基金', '2016-01-01', '', 0, 0, ''],
#        ['159920', '恒生ETF', '2016-09-01', '', 0, 0, ''],
#        ['510900', 'H股ETF', '2016-09-01', '', 0, 0, ''],
#        ['600663', '陆家嘴', '2016-12-01', '', 0, 0, ''],
#	['601668', '中国建筑', '2016-12-01', '', 0, 0, ''],
#        ['002673', '西部证券', '2016-12-01', '', 0, 0, ''],
#	['300104', '乐视网', '2016-12-01', '', 0, 0, ''],
#        ['300027', '华谊兄弟', '2016-12-01', '', 0, 0, ''],
#        ['300251', '光线传媒', '2016-12-01', '', 0, 0, ''],
#        ['000938', '紫光股份', '2016-12-01', '', 0, 0, ''],
#        ['600839', '四川长虹', '2016-12-01', '', 0, 0, ''],
#        ['002308', '威创股份', '2016-12-01', '', 0, 0, ''], # 幼儿教育产业
#        ['002638', '勤上光电', '2016-12-01', '', 0, 0, ''],

#        ['511010',  '国债ETF', '2016-12-01', '', 0, 0, ''],
#        ['600547', '山东黄金', '2016-11-01', '', 0, 0, ''],
#        ['000799', '酒鬼酒', '2016-09-01', '', 0, 0, ''],
#        ['600779', '水井坊', '2016-09-01', '', 0, 0, ''],
]

stocks2=[
        ['000002', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000063', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000333', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000403', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000418', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000429', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000488', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000513', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000538', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000568', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000596', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000651', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000710', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ]
stocks3=[
        ['000711', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000820', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000858', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000963', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['000981', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002008', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002032', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002035', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],	
        ['002085', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002110', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002127', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002142', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002206', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
	]
stocks4=[
        ['002210', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002304', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002311', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002372', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002415', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002450', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002460', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002466', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002475', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002507', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002508', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002569', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002572', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002597', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002635', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['002647', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],	
        ['002694', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['300072', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['300136', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['300156', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
]
stocks5=[
        ['300176', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['300296', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600036', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600197', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600258', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600276', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600298', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600309', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600377', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600452', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600487', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600519', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600622', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600779', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600809', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600816', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['600900', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],	
        ['601012', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['601238', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['601318', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
        ['601398', '恒瑞医药', '2014-01-01', '', 100000, 8, '2017-01-01'],
	] 

def new_weekly_policy (stock, data, total_money=100000, deal_count=8, first_buy=''):
        # global next_buy, selling_good_deals, next_half_buy, next_steady_buy
        # global global_tendency, lodgers, total_op_count, total_cost
        # global deal_cost, total_money, do_half_buy, do_steady_buy
        # global show_detail, show_signal, show_summary, show_verbose

        lodgers=None

        if deal_count == 0: # fast return
                return

        only_lastest_weeks = 5000 # lastest 50 weeks
        selling_good_deals=-1
        with_profit=0.06
        force_selling_good_deals=-1 # if total_cost is reach, then sell profit more than 10%
        forced_with_profit=0.6
        next_buy=-1
        next_half_buy=-1  # buy half cost when globa_tendency=1 and close_s=1
        next_steady_buy=-1 # buy one cost
        global_tendency=0
#        deal_cost=37000 # calculated from input total_money
#        deal_count=8  # at most this many deals # input argument with default value
        deal_cost = total_money / deal_count
        # total_money=deal_count * deal_cost # all of my money
        total_cost=0 # total cost of holding until now, must be less than total_money
        current_profit=0
        do_half_buy=0
        do_steady_buy=1
        show_detail=0
        show_signal=1
        show_summary=0
        total_op_count=0
        show_verbose=0
        profit_invested=1  # using profit to buy more stocks
        profit_multi=3 # must left that much as cash
        virt_profit=0 # all profit since time 0
        virt_total=0 # current holding shares value plut virtal profit
        sold_value=0 # saved all sold shares until now

        count = data['signal'].count()
        # if no volume, return now
        if count < 1 or data['Volume'][count-1] == 0:
                return

        # if non-empty, buy at no early that it else use the start date
        first_buy_at = data.index[0] if len(first_buy) == 0 else first_buy #pandas.datetime.strptime(first_buy, '%Y-%m-%d')

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
                   sold_value += data['Open'][i] * to_sold_deals['count'][j]
                   l_profit = (data['Open'][i]-to_sold_deals['price'][j])*to_sold_deals['count'][j]
                   lodgers.loc[to_sold_deals.index[j]]['profit']= l_profit
                   lodgers.loc[to_sold_deals.index[j]]['profit-rate']=lodgers.loc[to_sold_deals.index[j]]['profit']/lodgers.loc[to_sold_deals.index[j]]['total']
                   total_cost -= lodgers.loc[to_sold_deals.index[j]]['total']
                   current_profit += lodgers.loc[to_sold_deals.index[j]]['profit']

                   virt_profit += l_profit

                   # only update when first buy. 
                   # lodgers.loc[to_sold_deals.index[j]]['virt-total']=virt_total
                   # lodgers.loc[to_sold_deals.index[j]]['virt-profit']=virt_profit
                   
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

            if first_buy_at < data.index[i] :
                    new_row_data=pandas.DataFrame(index=data.index[i:i+1],
                                                  columns=['price',
                                                       'count',
                                                       'total',
                                                       'total-cost',
                                                       'virt-total',
                                                       'virt-profit',
                                                       'sell-date',
                                                       'sell-price',
                                                       'profit',
                                                       'profit-rate',
                                                       'pending-rate'])

                    new_row_data['price'][0]=data['Open'][i]
                    new_row_data['virt-total'][0]=0
                    new_row_data['virt-profit'][0]=0
                    new_row_data['pending-rate'][0]=0

                    if (next_buy > 0 or next_half_buy > 0 or next_steady_buy > 0):
                        count=int(deal_cost / data['Open'][i]/100.0) * 100
                        if next_half_buy > 0 and count >= 200:
                            count=count / 2
                        new_row_data['count'][0]=count
                        new_row_data['total'][0]=new_row_data['count'][0] * data['Open'][i]
                        #        new_row_data['signal'][0]=0
                        #        new_row_data['close_s'][0]=0
                        new_row_data['sell-date'][0]=0
                        new_row_data['sell-price'][0]=0
                        new_row_data['profit'][0]=0
                        new_row_data['profit-rate'][0]=0
                        new_row_data['pending-rate'][0]=0
                        total_cost += new_row_data['total'][0]
                        new_row_data['total-cost'][0]=total_cost

                        # exclude current cost from sold_value
                        if sold_value > 0:
                                sold_value -= new_row_data['total'][0]

                    if isinstance(lodgers, type(None)):
                            lodgers=new_row_data
                    else:
                            lodgers=lodgers.append(new_row_data)
                    
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

            if not isinstance(lodgers, type(None)):
                    l_deals=lodgers.select(lambda x: True if lodgers.loc[x]['sell-price'] == 0 else False)
                    if l_deals['sell-price'].count() > 0:
                            # select all pending share, calculate their virtual total value according to current price
                            cur_price = data.iloc[i]['Open']
        
                            l_virt_total=l_deals['count'].sum() * cur_price + sold_value

                            lodgers.iloc[lodgers['virt-total'].count() - 1]['virt-total'] = l_virt_total
                            lodgers.iloc[lodgers['virt-total'].count() - 1]['virt-profit'] = virt_profit
        

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
                print ' buy +%d, at %f' % (count, data.iloc[last]['Adj Close'])
        if (total_op_count != 0):
                print 'sell %d, at %f' % (total_op_count, data.iloc[last]['Adj Close'])
        if show_summary > 0 and not isinstance(lodgers, type(None)):
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

        if isinstance(lodgers, type(None)):
                return
        
        # calculate pending-rate now
        for i in range(lodgers['price'].count()):
                if lodgers.iloc[i]['sell-price'] > 0:
                        continue

                lodgers.iloc[i]['pending-rate'] = '%0.2f' % ((data.iloc[data['Open'].count()-1]['Adj Close']-lodgers.iloc[i]['price'])/lodgers.iloc[i]['price'])

        lodgers.to_csv('%s-lodgers.csv' % stock)

        if show_detail > 0:
            print lodgers

ppservers = ()
jobs = []

job_server = pp.Server(ppservers=ppservers)

def local_func1(stock, start, end):
        #StockSignal.stock_signal_w_new_find_candidate(stock, start, end)
        return StockSignal.stock_signal_w_new(stock, start, end).sort_index()

def local_func_d(stock, start, end):
        StockSignal.stock_signal_d_new_find_candidate(stock, start, end)

def one_stock(stock, start, end):
        print stock,start, end
        data = local_func1(stock, start, end)
        #data = pandas.read_csv('%sw-all-data.csv' % stock, index_col=0).sort_index()

        new_weekly_policy(stock, data, total_money=stocks[0][4], deal_count=stocks[0][5], first_buy=stocks[0][6])        


#        plot_data=data[['EMA', 'signal']][-60:]
#        plot_data['EMA']=plot_data['EMA']/max(plot_data['EMA']) * 10
        plot_data=data[['price', 'signal']]#[-60:]
        plot_data['price']=plot_data['price']/max(plot_data['price']) * 10

	count=plot_data['price'].count()
        up_data=[ 1 if a > 0 else 0 for a in plot_data['signal'] ] * plot_data['price']
        down_data=[ 1 if a < 0 else 0 for a in plot_data['signal'] ] * plot_data['price']

        _style = 'bar'
        
        # plot as point
        if cmp(_style, 'point') == 0 :
	        pyplot.plot(range(count), plot_data['price'], '.')
                pyplot.plot(range(count), up_data, '^')
                pyplot.plot(range(count), down_data, 'v')
                pyplot.plot(range(count), plot_data['signal'])
        elif cmp(_style, 'bar') == 0 :
		pyplot.bar(range(count),plot_data['price'], label='code = %s (%d/%d)' % (stock, 1, 1))
		pyplot.bar(range(count),up_data, label='buy')
		pyplot.bar(range(count),down_data, label='sell')
                #pyplot.bar(range(count),plot_data['signal'])
                pyplot.legend(loc='upper left')

	pyplot.title(stock)
	pyplot.savefig('%s.png' % stock)
	pyplot.close()

        new_weekly_policy(stock, data, total_money=stocks[0][4], deal_count=stocks[0][5], first_buy=stocks[0][6])

def one_stock_d(stock, start, end):
        data = local_func_d(stock, start, end)
        #data = pandas.read_csv('%sd-all-data.csv' % stock, index_col=0).sort_index()

        print stock
        new_weekly_policy(stock, data)

def all_stocks():
        stocks_count = 0
	_stocks=tushare.get_stock_basics()
        for s in _stocks.index:
                if _stocks.ix[s].profit <= 0:
                        continue

                if not path.exists('selected/%s.png' %s):
                        continue

                stocks_count+=1
                jobs.append(job_server.submit(local_func1, (s, stocks[0][2], stocks[0][3]), (), ("StockSignal", "pandas", )))

	pyplot.ioff()
	pyplot.figure(figsize=(18,6))
        start = 0
        for s in _stocks.index:
                if _stocks.ix[s].profit <= 0:
                        continue

                if not path.exists('selected/%s.png' % s):
                        continue
                
		csv_file='%sw-all-data.csv' % s
		while not path.exists(csv_file):
			print 'waiting for %s' % csv_file
			time.sleep(1)

                data=pandas.read_csv(csv_file, index_col=0).sort_index()

                print _stocks.ix[s].name
                plot_data=data[['price', 'signal']]#[-60:]
                plot_data['price']=plot_data['price']/max(plot_data['price']) * 10
                #figure=plot_data.plot(kind='bar',figsize=(12,6),title='%s' % s[0]).figure
                #figure.savefig('%s-%s.png' % (s, _stocks.ix[s].name), bbox_inches='tight')
                #figure=None
		count=plot_data['price'].count()
                up_data=[ 1 if a > 0 else 0 for a in plot_data['signal'] ] * plot_data['price']
                down_data=[ 1 if a < 0 else 0 for a in plot_data['signal'] ] * plot_data['price']

                start += 1
		pyplot.bar(range(count),plot_data['price'], label='code = %s (%d/%d)' % (s, start, stocks_count))
		pyplot.bar(range(count),up_data, label='buy')
		pyplot.bar(range(count),down_data, label='sell')
                #pyplot.bar(range(count),plot_data['signal'])
                pyplot.legend(loc='upper left')
                
		pyplot.title(s)
		pyplot.savefig('%s.png' % s)
		pyplot.clf() # clear current figure
                
                new_weekly_policy(s, data, total_money=stocks[0][4], deal_count=stocks[0][5], first_buy=stocks[0][6])

def __main():
#        stocks = stocks3
        
        for s in stocks:
                if s[5] == 0:  # deal_cost is zero, continue
                        continue
                jobs.append(job_server.submit(local_func1, (s[0], s[2], s[3]), (), ("StockSignal", "pandas", )))

        job_server.wait()
        print ''
        job_server.print_stats()
	
	pyplot.ioff()
        #use pp for following computing is not so good
	start=0
	stocks_count = len(stocks)
	pyplot.figure(figsize=(15,6*stocks_count))
        for s in stocks:
                if s[5] == 0: # deal_cost is zero, continue
                        continue
                data=pandas.read_csv('%sw-all-data.csv' % s[0], index_col=0).sort_index()

                print s[1],s[0]
#                plot_data=data[['EMA', 'signal']][-60:]
#                plot_data['EMA']=plot_data['EMA']/max(plot_data['EMA']) * 10
                plot_data=data[['price', 'signal']]#[-60:]
                plot_data['price']=plot_data['price']/max(plot_data['price']) * 10
                #figure=plot_data.plot(kind='bar',figsize=(12,6),title='%s' % s[0]).figure
                #figure.savefig('%s-%s.png' % (s[0], s[1]), bbox_inches='tight')
                #figure=None
		start+=1
		pyplot.subplot(stocks_count, 1, start)
		count=plot_data['price'].count()
                up_data=[ 1 if a > 0 else 0 for a in plot_data['signal'] ] * plot_data['price']
                down_data=[ 1 if a < 0 else 0 for a in plot_data['signal'] ] * plot_data['price']

                _style = 'bar'

                # plot as point
                if cmp(_style, 'point') == 0 :
	                pyplot.plot(range(count), plot_data['price'], '.')
                        pyplot.plot(range(count), up_data, '^')
                        pyplot.plot(range(count), down_data, 'v')
                        pyplot.plot(range(count), plot_data['signal'])
                elif cmp(_style, 'bar') == 0 :
                        tt = u'code = %s %s (%d/%d)' % (s[0], s[1].decode('utf-8'), start, stocks_count)
		        pyplot.bar(range(count),plot_data['price'], label=tt)
		        pyplot.bar(range(count),up_data, label='buy')
		        pyplot.bar(range(count),down_data, label='sell')
                        #pyplot.bar(range(count),plot_data['signal'])
                        pyplot.legend(loc='upper left')

		pyplot.title(s[0])

                if s[4] > 0:
                        new_weekly_policy(s[0], data, total_money=s[4], deal_count=s[5], first_buy=s[6])
                else:
                        new_weekly_policy(s[0], data, deal_count=s[5], first_buy=s[6])
	pyplot.subplots_adjust(left=0.05, top=0.99, bottom=0.01, right=0.95, hspace=0.1, wspace=0.1) 
	pyplot.savefig('stocks.png')
	pyplot.close()

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

#pandas.read_csv('510300w-all-data.csv', index_col=0)[['EMA', 'signal']][-60:].plot(kind='bar',figsize=(20,12),title='ETF300').figure.show()
#figure.savefig('a.svg', format='svg', bbox_inches='tight')

def main(argv):
    print argv

    mpl.rcParams['font.sans-serif'] = ['AR PL KaitiM GB'] # SimHei is common Chinese font on macOS. ttc is not ok.
#fonts-arphic-gkai00mp/xenial 2.11-15 all
#  "AR PL KaitiM GB" Chinese TrueType font by Arphic Technology

# after install new font, must delete this file: /root/.cache/matplotlib/fontList.cache  to let matplotlib update font cache

    if len(argv) == 1:
        __main()
        return

    # 1 args: all_stocks
    if len(argv) == 2:
            globals()[argv[1]]()
    # 2 args: one_stock ######, last year
    elif len(argv) == 3:
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
