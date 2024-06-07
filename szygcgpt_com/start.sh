#!/bin/bash
nohup /root/anaconda3/envs/python38/bin/python feizhaobiao.py >> ./feizhaobiao`date +%Y-%m-%d`.out 2>&1 & echo $! > feizhaobiao.pid
nohup /root/anaconda3/envs/python38/bin/python zhaobiao.py >> ./zhaobiao`date +%Y-%m-%d`.out 2>&1 & echo $! > zhaobiao.pid

