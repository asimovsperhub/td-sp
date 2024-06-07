import os
import sys

import requests

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


from crawldata_spider.tools.WxNotify import WxNotify

wx = WxNotify()


def to_messages(user_id, content):
    """
    ws
    :param user_id:
    :param content:
    :return:
    """
    url = "http://42.193.247.183:30300/api/v1/msg/sendWs"
    data = {
        "userId": user_id,
        "content": content
    }
    res = requests.post(url=url, data=data)
    print(res.text)


def send_messages(to, sub_type, title, keywords, city, sql_id, message_type=None):
    data = {
        "first": {
            "value": "监测结果",
            "color": "#173177"
        },
        "keyword1": {
            "value": sub_type,
            "color": "#173177"
        },
        "keyword2": {
            "value": title,
            "color": "#173177"
        },
        "keyword3": {
            "value": keywords,
            "color": "#173177"
        },
        "keyword4": {
            "value": city,
            "color": "#173177"
        },
        "remark": {
            "value": f"备注",
            "color": "#173177"
        }
    }
    if message_type == "wx":
        wx.send_template_message(to,
                                 f"https://yixianghuitong.com/biddingInformation/{sql_id}",
                                 data)
    else:
        to_messages(to, f"{sub_type}-{city}-{keywords}:https://yixianghuitong.com/biddingInformation/{sql_id}")


if __name__ == '__main__':
    to_messages(55, "测试")
