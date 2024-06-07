import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from tools import tools
from ygp_gdzwfw_gov_cn.disclosure import Ygp
from zfcg_szggzy_com.intention import Intention
from szygcgpt_com.notender import YGCG_NoTender
from szygcgpt_com.tender import YGCG_Tender
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
import setting

# 配置日志显示
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='a')


# 调度器异常
def listener(event):
    if event.exception:
        print('任务出错了！！！！！！')
    else:
        print('任务照常运行...')


scheduler = BlockingScheduler()

# 深圳阳光采购平台
tender = YGCG_Tender(thread_count=1)
scheduler.add_job(func=tender.start, trigger='interval', seconds=60 * 10, id='ygcp_tender_interval_task')
# notender = YGCG_NoTender(thread_count=1)
# scheduler.add_job(func=notender.start, trigger='interval', seconds=60 * 10, id='ygcp_notender_interval_task')

# 中国·深圳政府采购-意向公告
intention = Intention(thread_count=1)
scheduler.add_job(func=intention.start, trigger='interval', seconds=60 * 5, id='zfcg_intention_interval_task')

# 广东省公共资源
ygp = Ygp(thread_count=1)
# interval 固定的时间间隔触发事件
scheduler.add_job(func=ygp.start, trigger='interval', seconds=60 * 5, id='ygp_interval_task')

scheduler.add_job(func=tools.set_sub_redis, trigger='interval', seconds=60, id='set_sub_redis_task')

# 配置任务执行完成和执行错误的监听
scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

# 设置日志
scheduler._logger = logging

if __name__ == '__main__':
    scheduler.start()
