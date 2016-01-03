
import urllib 
import urllib2 
import requests
url='http://real-chart.finance.yahoo.com/table.csv?s=002673.SZ&a=0&b=1&c=2015&d=11&e=31&f=2016&g=w&ignore=.csv'
urllib.urlretrieve(url, "002673w.csv")
