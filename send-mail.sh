#!/bin/bash

cat $1 | mailx -S'smtp=smtp.sina.com' -S'smtp-auth=login' -S'smtp-auth-user=nkwilson' -S'smtp-auth-password=1qaz2wsx' -r nkwilson@sina.com -s "Robot: $1" -. nkwilson@sina.com
sleep 1
for i in *.pdf ; do
    echo $i | mailx -S'smtp=smtp.sina.com' -S'smtp-auth=login' -S'smtp-auth-user=nkwilson' -S'smtp-auth-password=1qaz2wsx' -r nkwilson@sina.com -a $i -s "Robot: $i" -. nkwilson@sina.com
    sleep 1
done
