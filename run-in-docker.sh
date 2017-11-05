#!/bin/bash

bash core-work.sh > summary && ls -l *.png && \
 bash send-mail.sh summary


