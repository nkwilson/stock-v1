import pandas
import tushare
import StockSignal

stocks=tushare.get_stock_basics()

for i in range(stocks['name'].count()):
 print i
 try:
  data=StockSignal.stock_signal_w_new(stocks.index[i], '2014-01-01', '2017-03-10')
  if data['EMA'].count() < 60:
      del(data)
      continue
  if data['signal'].sum() < 1:
      del(data)
      continue
  figure=data[['EMA', 'signal']][-60:].plot(kind='bar',figsize=(12,6), title='%s %s' % (stocks.ix[i].name, stocks.index[i])).figure
  figure.savefig('%s.png' % stocks.index[i], bbox_inches='tight')
  del(figure)
 except Exception, ex:
  pass
