import datetime
import os
import re
import sys
import time

import feapder
from lxml import etree
import tools

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from crawldata_spider.tools.message import send_messages
from crawldata_spider.tools.zinc import push
from crawldata_spider.tools.db import MysqlDb
from crawldata_spider.tools.tools import list2str, format_sql_value, parse_sub, parseWx_sub
from crawldata_spider.tools import tools, redis_cli

"""
意向公告
"""


class Intention(feapder.AirSpider):

    def start_requests(self):
        for page in range(1, 11):
            if page == 1:
                url = "http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001002/purchase_intention.html"
            else:
                url = f"http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001002/{page}.html"
            time.sleep(0.8)
            yield feapder.Request(url, callback=self.parse, verify=False, method="GET", request_sync=True)

    def download_midware(self, request):
        request.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "http://zfcg.szggzy.com:8081/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            # "User-Agent": str(UserAgent(verify_ssl=False).random)
        }
        request.cookies = {
            "userGuid": "1047923792",
            "oauthClientId": "admin",
            "oauthPath": "http://127.0.0.1:8080/EpointWebBuilder",
            "oauthLoginUrl": "http://127.0.0.1:1112/membercenter/login.html?redirect_uri=",
            "oauthLogoutUrl": "",
            "fontZoomState": "0",
            "noOauthRefreshToken": "27bb125a030de3d0da81454b9f710e7a",
            "noOauthAccessToken": "066979910bc74737e92be6621b92c0e6"
        }
        pro = tools.get_proxy()
        request.proxies = pro
        return request

    # 采购意向公告
    def parse(self, request, response):

        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//tbody[@id="list"]//tr')
        for tr in trs:
            info = {}
            info["bulletin_type"] = "意向公告"
            info["industry_classification"] = "政府采购"
            info["city"] = "深圳市"
            info["title"] = tr.xpath("./td[2]/text()")[0]
            info["release_time"] = tr.xpath("./td[5]/text()")[0].strip() + " 00:00:00"
            info["bidopening_time"] = tr.xpath("./td[6]/text()")[0] + "-28 00:00:00"  # 预计采购时间
            info["amount"] = tr.xpath("./td[3]/text()")[0]  # 金额
            info["tender_name"] = tr.xpath("./td[4]/text()")[0]  # 采购单位
            info["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if tr.xpath("./td[7]/a/@href"):
                if not redis_cli.get_cache("zfcg_" + info["title"]):
                    info["link"] = tr.xpath("./td[7]/a/@href")[0]
                    time.sleep(0.8)
                    print(info["link"])
                    yield feapder.Request(info["link"], callback=self.parse_details,
                                          info=info, download_midware=self.download_details, request_sync=True)

    def download_details(self, request):
        request.cookies = {
            'userGuid': '-2001935666',
            'Hm_lvt_42d6d6c9d2c97bcda19906bdfe55f5c0': '%d' % int(time.time()),
            'fontZoomState': '0',
            'oauthClientId': 'admin',
            'oauthPath': 'http://127.0.0.1:8080/EpointWebBuilder',
            'oauthLoginUrl': 'http://127.0.0.1:1112/membercenter/login.html?redirect_uri=',
            'oauthLogoutUrl': '',
            'noOauthRefreshToken': '72e6d3447a1ec39429d5639c966dbd66',
            'noOauthAccessToken': '5f3843679403e7f3149e1db3439d81dd',
        }

        request.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'If-Modified-Since': 'Wed, 12 Apr 2023 08:22:13 GMT',
            'If-None-Match': 'W/"64366a35-1b14"',
            'Referer': 'http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001002/purchase_intention.html',
            'Upgrade-Insecure-Requests': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        pro = tools.get_proxy()
        request.proxies = pro
        return request

    def parse_details(self, request, response):
        info = request.info
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//div[@class="contentbox"]//text()')
        if trs:
            info["announcement_content"] = "\n".join(trs)
            info["contact_person"] = trs[-7]
            info["contact_information"] = trs[-5]
            insert_ignore = False
            sql = "insert%s into `{table}` {keys} values {values}" % (
                " ignore" if insert_ignore else ""
            )
            keys = ["`{}`".format(key) for key in info.keys()]
            keys = list2str(keys).replace("'", "")
            values = [format_sql_value(value) for value in info.values()]
            values = list2str(values)
            sql = sql.format(table="bidding", keys=keys, values=values).replace("None", "")
            print(sql)
            _, id = MysqlDb().add(sql)
            if id:
                print(id)
                push(info, id)
                print("中国·深圳政府采购-意向公告-开始微信订阅------------------->")
                for sub in parseWx_sub():
                    print("微信id----------->", sub)
                    if info.get("bulletin_type") == sub[1]:
                        if info.get("city") in sub[2]:
                            for i in sub[3].split(","):
                                match = re.search("%s.*?" % i, info["announcement_content"])
                                print("match--------->", match)
                                if match:
                                    send_messages(to=sub[0], sub_type=sub[1], title=info.get("title"), keywords=i,
                                                  city=info.get("city"),
                                                  sql_id=id, message_type="wx")
                print("中国·深圳政府采购-意向公告-开始个人中心订阅------------------->")
                for sub in parse_sub():
                    print("用户id----------->", sub[0])
                    if info.get("bulletin_type") == sub[1]:
                        if info.get("city") in sub[2]:
                            for i in sub[3].split(","):
                                match = re.search("%s.*?" % i, info["announcement_content"])
                                print("match--------->", match)
                                if match:
                                    send_messages(sub[0], sub_type=sub[1], title=info.get("title"), keywords=i,
                                                  city=info.get("city"),
                                                  sql_id=id)
                redis_cli.set_cache("zfcg_" + info.get("title"), 1, ex=60 * 60 * 24 * 3)


if __name__ == "__main__":
    Intention(thread_count=1).start()
