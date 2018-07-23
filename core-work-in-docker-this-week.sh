set -xe

TMPD=$(mktemp -d)
CURD=$(pwd)

cd $TMPD
cat - > Dockerfile <<EOF
from ubuntu:tushare-16.04

volume /stock 
workdir /stock

cmd WDIR="\$(date '+%Y%m%d')" && mkdir \$WDIR && cd \$WDIR && pwd && bash ../core-work.sh

EOF

docker build -t ubuntu:core-work-cmd.sh .
cd ..

docker run --rm -v $(pwd):/stock ubuntu:core-work-cmd.sh
