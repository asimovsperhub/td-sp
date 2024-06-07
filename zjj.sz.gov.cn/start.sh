#!/bin/bash
nohup /root/anaconda3/envs/python38/bin/python xxgk.py >> ./xxgk.`date +%Y-%m-%d`.out 2>&1 & echo $! > xxgk..pid