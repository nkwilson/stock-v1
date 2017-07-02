import sys
import getopt

import pandas
import datetime

import StockPrice


if sys.flags.debug != 0:
    print sys.flags.debug
    print len(sys.argv), sys.argv

if len(sys.argv) != 2: # first arg is stock code
  print 'Usage: %s stock-code' % sys.argv[0]
  sys.exit(0)

start=pandas.datetime.now()
if start.weekday() > 4:
    start+=datetime.timedelta(-start.weekday())
else:
    start+=datetime.timedelta(-7)

end=start+datetime.timedelta(4)

if sys.flags.debug != 0:
    print start, end

print StockPrice.StockPrice_4(sys.argv[1], 'w', start, end)
