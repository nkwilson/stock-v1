#!/bin/bash

echo $LANG
echo $LC_ALL

bash core-work.sh > summary
bash send-mail.sh summary


