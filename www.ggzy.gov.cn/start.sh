#!/bin/bash
# nohup /root/anaconda3/envs/python38/bin/python ggzyhis.py >> ./ggzyhis`date +%Y-%m-%d`.out 2>&1 & echo $! > ggzyhis.pid
nohup /root/anaconda3/envs/python38/bin/python ggzyzcfg.py >> ./ggzyzcfg`date +%Y-%m-%d`.out 2>&1 & echo $! > ggzyzcfg.pid