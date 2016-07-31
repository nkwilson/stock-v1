if [ "${OSTYPE}" = "darwin15" ]; then
export PYTHONPATH=/usr/local/lib/python2.7/site-packages
fi

python2.7 scan-these-stocks.py
python2.7 scan-this-funds.py
