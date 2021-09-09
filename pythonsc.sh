#!/bin/sh

python3 temp.py &
python3 slave.py &
python3 master.py &
python3 plot.py

wait
