import json
import os
import sys
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
import requests
from Scheduled.utils import redis_cli

# 微信公众号配置
WECHAT_TOKEN = "cloud"  # 微信的token令牌,和配置时的token要统一
WECHAT_APPID = "wx2fc17e10f214c227"  # appID
WECHAT_APPSECRET = "5fbcc4059b229fe53cb3b2ae1c6fb583"  # AppSecret

class WxNotify:
    def __init__(self):
        self.access_token = self.get_access_token()
        self.url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}" \
            .format(access_token=self.access_token)

    def get_access_token(self):
        if redis_cli.get_cache("wx_access_token"):
            return redis_cli.get_cache("wx_access_token")
        else:
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}" \
                .format(appid=WECHAT_APPID, appsecret=WECHAT_APPSECRET)
            response = requests.get(url=url).json()
            print(response)
            access_token = response["access_token"]
            redis_cli.set_cache("wx_access_token", access_token, ex=60 * 115)
            return access_token

    def send_template_message(self, openid, url: str, data: dict):
        post_dict = {
            "touser": openid,
            "template_id": "x3016xxgaPxxMowAOTH_gA_dkKC819iXR9tIhq3Gjvs",
            "url": url,
            "data": data,
        }
        post_dict = json.dumps(post_dict)
        try:
            response = requests.post(self.url, data=post_dict)
            data = response.json()
            if data.get("errcode") == 0:
                return True
        except Exception as e:
            return False


if __name__ == '__main__':
    wx = WxNotify()
    data = {
        "first": {
            "value": "监测结果",
            "color": "#173177"
        },
        "keyword1": {
            "value": "账户名称",
            "color": "#173177"
        },
        "keyword2": {
            "value": "账户站点",
            "color": "#173177"
        },
        "keyword3": {
            "value": f"关键词",
            "color": "#173177"
        },
        "keyword4": {
            "value": f"监测结果",
            "color": "#173177"
        },
        "remark": {
            "value": f"备注",
            "color": "#173177"
        }
    }
    wx.send_template_message("oG9oT5z3wAUzcjYKdOIdzM88zDSY", "url", data)
