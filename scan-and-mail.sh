#!/bin/bash
bash scan.sh | tee result.log
[ -s result.log ] && mail -r yubin@h3c.com -s 'selected ' nkwilson@sina.com < result.log

