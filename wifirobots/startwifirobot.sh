#!/bin/sh
# For start in foreground
python3 /home/pi/work/wifirobots/python_src/hbwz_startmain.py
# For start in background
# nohup python3 /home/pi/work/wifirobots/python_src/hbzw_startmain.py &

sleep 12

node /home/pi/work/wifirobots/XiaoRGeekBle/code/XiaoRGeek/main.js &
exit 0
#./wifirobots &



