if [ "${OSTYPE}" = "darwin15" ]; then
export PYTHONPATH=/usr/local/lib/python2.7/site-packages
fi

python2.7 scan-these-stocks.py > /dev/null 2>&1 # output: scan-these-funds-candidates-%Y-%m-%d.csv
python2.7 scan-this-funds.py   2>&1 > /dev/null # output: scan-this-funds-candidates-%Y-%m-%d.csv
python2.7 scan-fenji-funds-for-candidate.py 2>&1 > /dev/null # output: fenji-funds-candidates-%Y-%m-%d.csv

suffix=$(date +%Y-%m-%d)

if [ "${OSTYPE}" = "darwin15" -o "${OSTYPE}" = "darwin16" ]; then
    last_fri=$(date -v-fri +%Y-%m-%d)
else
    last_fri=$(date +%Y-%m-%d --date="Fri")
fi

week_day=$(date +%w)
last_key_day=$(date +%Y-%m-%d)

if [ "${week_day}" -ge "5" ]; then
    last_key_day=$last_fri
fi

# python2.7 select-based-weekly-candidate.py select_base_weekly_candidate scan-these-stocks-candidates-${suffix}.csv "${last_key_day}"
# python2.7 select-based-weekly-candidate.py select_base_weekly_candidate scan-this-funds-candidates-$suffix.csv "${last_key_day}"
# python2.7 select-based-weekly-candidate.py select_base_weekly_candidate fenji-funds-candidates-$suffix.csv "${last_key_day}"

python2.7 new-weekly-policy.py

