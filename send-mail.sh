#!/bin/bash

cat $1 | mailx -Ssmtp-use-starttls -S'ssl-protocol=-ALL,+TLSv1.2' -S'ssl-verify=strict' -Ssendwait -S'smtp=smtps://smtp.sina.com:465' -S'smtp-auth=login' -S'smtp-auth-user=nkwilson' -S'smtp-auth-password=1qaz2wsx' -r nkwilson@sina.com -s "Robot: $1" -. nkwilson@sina.com
for i in *.pdf ; do
    echo $i | mailx -Ssmtp-use-starttls -S'ssl-protocol=-ALL,+TLSv1.2' -S'ssl-verify=strict' -Ssendwait -S'smtp=smtps://smtp.sina.com:465' -S'smtp-auth=login' -S'smtp-auth-user=nkwilson' -S'smtp-auth-password=1qaz2wsx' -r nkwilson@sina.com -a $i -s "Robot: $i" -. nkwilson@sina.com
done
