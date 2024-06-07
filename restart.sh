#!/bin/bash
ps -ef | grep crawl_main.py | grep -v grep | awk '{print $2}' | xargs kill -9
echo "已关闭mian"
nohup  /root/anaconda3/envs/python38/bin/python crawl_main.py >> ./nohup.out 2>&1 &
echo "已启动mian"