#!/bin/bash
nohup /root/anaconda3/envs/python38/bin/python /mnt/crawldata_spider/szcg/szcg1.py >> /mnt/crawldata_spider/szcg/szcg1`date +%Y-%m-%d`.out 2>&1 &
nohup /root/anaconda3/envs/python38/bin/python /mnt/crawldata_spider/szcg/szcg2.py >> /mnt/crawldata_spider/szcg/szcg2`date +%Y-%m-%d`.out 2>&1 &
nohup /root/anaconda3/envs/python38/bin/python /mnt/crawldata_spider/szcg/szcg3.py >> /mnt/crawldata_spider/szcg/szcg3`date +%Y-%m-%d`.out 2>&1 &