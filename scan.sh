if [ "${OSTYPE}" = "darwin15" ]; then
export PYTHONPATH=/usr/local/lib/python2.7/site-packages
fi

#python2.7 scan-these-stocks.py > /dev/null 2>&1 # output: scan-these-funds-candidates-%Y-%m-%d.csv
#python2.7 scan-this-funds.py   2>&1 > /dev/null # output: scan-this-funds-candidates-%Y-%m-%d.csv
#python2.7 scan-fenji-funds-for-candidate.py 2>&1 > /dev/null # output: fenji-funds-candidates-%Y-%m-%d.csv

suffix=$(date +%Y-%m-%d)

python2.7 select-based-weekly-candidate.py select_base_weekly_candidate scan-these-stocks-candidates-${suffix}.csv ${suffix}
python2.7 select-based-weekly-candidate.py select_base_weekly_candidate scan-this-funds-candidates-$suffix.csv $suffix
python2.7 select-based-weekly-candidate.py select_base_weekly_candidate fenji-funds-candidates-$suffix.csv $suffix
