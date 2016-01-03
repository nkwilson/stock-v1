import pandas

stocks=pandas.read_csv('stocks-code-name.csv', header=None)

for i in range(stocks[0].count()):
    code=stocks[0][i]
    stocks[0][i]='%06d.SZ' % code if code < 600000 else stocks[0][i]='%06d.SS' % code

stocks.to_csv('stocks-code.ex-name.csv')
