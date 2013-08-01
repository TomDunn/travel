#!/bin/bash

TZ='America/New_York'; export TZ
cd `dirname "${BASH_SOURCE[0]}"` && git pull && python Update.py && ./build.sh && echo `date` && echo "updated"
