#!/bin/bash

echo $LANG
echo $LC_ALL

bash core-work.sh > summary

cat summary
ls *.pdf

bash send-mail.sh summary


