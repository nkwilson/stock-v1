#!/bin/bash

bash core-work.sh > summary
bash -x send-mail.sh summary


