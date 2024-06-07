#!/bin/bash
# nohup /root/anaconda3/envs/python38/bin/python ccgptenderhis.py >> ./his`date +%Y-%m-%d`.out 2>&1 & echo $! > his.pid
nohup /root/anaconda3/envs/python38/bin/python ccgpconsultationhis.py >> ./ccgpconsultationhis`date +%Y-%m-%d`.out 2>&1 & echo $! > ccgpconsultationhis.pid