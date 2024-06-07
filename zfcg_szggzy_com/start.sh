#!/bin/bash
nohup /root/anaconda3/envs/python38/bin/python gsgg_cgyxgk.py >> ./gsgg_cgyxgk.`date +%Y-%m-%d`.out 2>&1 & echo $! > gsgg_cgyxgk..pid