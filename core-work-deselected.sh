#!/bin/bash

BASEDIR=$(dirname $(realpath $0))

export DISPLAY=:1
Xvfb :1 -screen 0 1024x768x16 &

python ${BASEDIR}/new_weekly_policy.py deselected

