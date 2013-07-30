#!/bin/bash

killall mynt

rm -rf _build/
mynt gen _build

mynt serve _build -p 8000 &
