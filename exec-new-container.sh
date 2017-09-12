#!/bin/bash

cat - > Dockerfile <<EOF
from ubuntu

EOF

# mail cmd
cat summary | mailx -S 'smtp=smtp.sina.com' -S'smtp-auth=login' -S'smtp-auth-user=nkwilson' -S'smtp-auth-password=1qaz2wsx' -r nkwilson@sina.com -a *.pdf -s 'robot ' -. nkwilson@sina.com 

