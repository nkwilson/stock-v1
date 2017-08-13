#!/bin/bash

export DISPLAY=:1
Xvfb :1 -screen 0 1024x768x16 &

python new_weekly_policy.py | tee summary

