#!/bin/bash

# run stock-v1
git clone -b adx https://github.com/nkwilson/stock-v1.git && cd stock-v1 && \
 bash core-work.sh > summary && \
 bash send-mail.sh summary


