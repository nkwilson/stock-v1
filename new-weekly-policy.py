# -*- coding: utf-8 -*-

import pandas
import numpy


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
        ['600663.SS', '陆家嘴'],
        ['000333.SZ', '美的集团'],
        ['002673.SZ', '西部证券'],
        ['002407.SZ', '多佛多'],
        ['002460.SZ', '赣锋锂业'],
        ['300017.SZ', '网宿科技'],
        ['300027.SZ', '华谊兄弟'],
        ['300251.SZ', '光线传媒'],
        ['000938.SZ', '紫光股份'],
        ['600547.SS', '山东黄金'],
        ['000799.SZ', '酒鬼酒'],
        ['600519.SS', '贵州茅台'],
        ['600779.SS', '水井坊'],
	['000002.SZ', '万科A'],
	['300104.SZ', '乐视网'],
	['000651.SZ', '格力电器'],
        ['600887.SS', '伊利股份'],
        ['600839.SS', '四川长虹'],
        ['002308.SZ', '威创股份'], # 幼儿教育产业
        ['002638.SZ', '勤上光电'],
        ['300160.SZ', '秀强股份'],
        ['510050.SS',  '50ETF'],
        ['510300.SS',  '300ETF'],
        ['510500.SS',  '500ETF'],
        ['511010.SS',  '国债ETF'],                    
        ['518800.SS', '黄金基金'],
        ['159920.SS', '恒生ETF'],
        ['510900.SS', 'H股ETF'],
        ['159915.SZ', '创业板'],
        ['159902.SZ', '中小板'],
        ['150023.SZ', '深成指B'],          
        ['150201.SZ', '券商B'],
        ['150153.SZ', '创业板B'],
]

def new_weekly_policy ():
        lodgers=None

        only_lastest_weeks = 5000 # lastest 50 weeks
        selling_good_deals=-1
        next_buy=-1
        next_half_buy=-1  # buy half cost when globa_tendency=1 and close_s=1
        next_steady_buy=-1 # buy one cost 
        global_tendency=0
        deal_cost=7000
        total_money=5*deal_cost # all of my money
        total_cost=0 # total cost of holding until now, must be less than total_money
        do_half_buy=0
        do_steady_buy=1
        show_detail=0
        show_signal=1
        show_summary=0
        total_op_count=0
        show_verbose=0

        count = data['signal'].count()
        for i in range(count):
            if show_verbose > 0 :
                print '### round %d' % i 
                print data.iloc[i][['open', 'volume']] 
            if data['volume'][i] == 0:
                continue

            if i < (count - only_lastest_weeks):
                continue
        
            if selling_good_deals == 0 and next_buy==0 and next_half_buy==0 and next_steady_buy == 0:
                continue

            if selling_good_deals > 0 and not isinstance(lodgers, type(None)):
                # find those holding deals, sell-price is empty
               deals=lodgers.select(lambda x: True if lodgers.loc[x]['sell-price'] == 0 else False)
               to_sold_deals=deals.select(lambda x: True if deals.loc[x]['price'] < data['open'][i] else False)
               if isinstance(to_sold_deals, type(None)):
                   continue;

               if show_verbose > 0 :
                print to_sold_deals[['price','count','total']]
                
               for j in range(to_sold_deals['price'].count()):
                   #           print data.index[i]
                   lodgers.loc[to_sold_deals.index[j]]['sell-date']=data.index[i]
                   lodgers.loc[to_sold_deals.index[j]]['sell-price']=data['open'][i]
                   lodgers.loc[to_sold_deals.index[j]]['profit']=(data['open'][i]-to_sold_deals['price'][j])*to_sold_deals['count'][j]
                   total_cost -= lodgers.loc[to_sold_deals.index[j]]['total']

               if show_verbose > 0 :
                print lodgers[['price','count','total','sell-date','sell-price']] 

            selling_good_deals=-1

            if next_buy > 0 or next_half_buy > 0 or next_steady_buy > 0:
                new_row_data=pandas.DataFrame(index=data.index[i:i+1], columns=['price', 'count', 'total', 'total-cost', 'sell-date', 'sell-price', 'profit'])
                new_row_data['price'][0]=data['open'][i]
                count=int(deal_cost / data['open'][i]/100.0) * 100
                if next_half_buy > 0 and count >= 200:
                    count=count / 2

                new_row_data['count'][0]=count
                new_row_data['total'][0]=new_row_data['count'][0] * data['open'][i]
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
                print 'signal %d close_s %d' % (data['signal'][i], data['close_s'][i]) 

            if data['signal'][i] < 0:
                selling_good_deals=1
            elif data['signal'][i] > 0:
                next_buy=1
            if data['close_s'][i] == 0:
                next_buy=1 if total_money > total_cost else 0
            elif global_tendency < 1:
                selling_good_deals=1
            elif do_half_buy > 0:
                next_half_buy=1
            elif do_steady_buy > 0:
                next_steady_buy=1

            global_tendency=data['signal'][i]

        # generate signal for next operation, buy and/or sell?
        if show_signal > 0:
            last=data['open'].count()-1
            price=data.iloc[last]['open']
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
            last=data['open'].count()-1
            count=int(deal_cost / data.iloc[last]['open']/100.0) * 100
            if next_half_buy > 0 and count >= 200:
                count=count / 2
            
            if count > 0 and total_op_count == 0:
                print '+%d' % count

        if (total_op_count != 0):
                print '%d' % total_op_count
        
        if show_verbose > 0 :
          print 'selling %d next_buy %d next_half_buy %d global %d' % (selling_good_deals, next_buy, next_half_buy, global_tendency) 

        if show_summary > 0:
            last=data['open'].count()-1
            price=data.iloc[last]['open']
            holdings=lodgers.select(lambda x: True if lodgers.loc[x]['sell-price']==0 else False)
            total_profit=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['profit'].sum()
            total_profit2=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['profit']/lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['total']
            total_flows=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['total'].sum()

            print '### flows %d profit %d rate %.3f rate2 %.3f holding %d(=%d) pending %d' % (total_flows, total_profit, total_profit/total_flows, total_profit2.sum() / total_profit2.count(),
                                                                                              holdings['count'].sum(), holdings['total'].sum(), holdings['count'].sum() * price - holdings['total'].sum())

        if show_detail > 0:
            print lodgers



for s in stocks:
     data=pandas.read_csv('%sw-all-data.csv' % s[0], index_col=0).sort_index()
     print s[1]
     new_weekly_policy()
        
