import pandas
import numpy

selling_good_deals=-1
next_buy=-1
global_tendency=0
deal_cost=14000
total_money=50000 # all of my money
total_cost=0 # total cost of holding until now, must be less than total_money

#data=pandas.read_csv('600547.SSw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('000799.SZw-all-data.csv', index_col=0).sort_index()
data=pandas.read_csv('000938.SZw-all-data.csv', index_col=0).sort_index()
#data=pandas.read_csv('600519.SSw-all-data.csv', index_col=0).sort_index()

lodgers=None

for i in range(data['signal'].count()):
#    print '### round %d' % i 
#    print data.iloc[i][['open', 'volume']]
    if data['volume'][i] == 0:
        continue
    
    if selling_good_deals == 0 and next_buy == 0:
       continue

    if selling_good_deals > 0 and not isinstance(lodgers, type(None)):
       # find those holding deals, sell-price is empty
       deals=lodgers.select(lambda x: True if lodgers.loc[x]['sell-price'] == 0 else False)
       to_sold_deals=deals.select(lambda x: True if deals.loc[x]['price'] < data['open'][i] else False)
       if isinstance(to_sold_deals, type(None)):
           continue;

#       print to_sold_deals[['price','count','total']]
       for j in range(to_sold_deals['price'].count()):
#           print data.index[i]
       	   lodgers.loc[to_sold_deals.index[j]]['sell-date']=data.index[i]
	   lodgers.loc[to_sold_deals.index[j]]['sell-price']=data['open'][i]
	   lodgers.loc[to_sold_deals.index[j]]['profit']=(data['open'][i]-to_sold_deals['price'][j])*to_sold_deals['count'][j]
           total_cost -= lodgers.loc[to_sold_deals.index[j]]['total']
           
#       print lodgers[['price','count','total','sell-date','sell-price']]

    selling_good_deals=-1
    
    if next_buy > 0:
        new_row_data=pandas.DataFrame(index=data.index[i:i+1], columns=['price', 'count', 'total', 'total-cost', 'sell-date', 'sell-price', 'profit'])
        new_row_data['price'][0]=data['open'][i]
        new_row_data['count'][0]=int(deal_cost / data['open'][i]/100.0) * 100
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

#    print 'signal %d close_s %d' % (data['signal'][i], data['close_s'][i])
    
    if data['signal'][i] < 0:
        selling_good_deals=1
    elif data['signal'][i] > 0:
        next_buy=1
    if data['close_s'][i] == 0:
        next_buy=1
    elif global_tendency < 1:
        selling_good_deals=1

    global_tendency=data['signal'][i]

#    print 'selling %d next_buy %d global %d' % (selling_good_deals, next_buy, global_tendency)

print lodgers

holdings=lodgers.select(lambda x: True if lodgers.loc[x]['sell-price']==0 else False)
total_profit=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['profit'].sum()
total_flows=lodgers.select(lambda x: True if lodgers.loc[x]['profit']>0 else False)['total'].sum()

print ''
print 'flows %d profit %d rate %.3f' % (total_flows, total_profit, total_profit/total_flows)
print ''
