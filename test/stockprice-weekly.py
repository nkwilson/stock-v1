import sys
import getopt

import StockPrice

print len(sys.argv), sys.argv

if len(sys.argv) != 4: # first arg is stock code
  print 'Usage: %s stock-code start-date end-date' % sys.argv[0]
  sys.exit(0)

data=StockPrice.StockPrice_4(sys.argv[1], 'w', sys.argv[2], sys.argv[3])
data.to_csv('%s-weekly-%s.csv' % (sys.argv[1], sys.argv[2]))
