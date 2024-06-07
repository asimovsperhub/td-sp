import datetime
import json
import os
import random
import re
import string
import sys
import time

import feapder

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from crawldata_spider.tools.message import send_messages
from crawldata_spider.tools.zinc import push
from crawldata_spider.tools.db import MysqlDb
from crawldata_spider.tools.tools import list2str, format_sql_value, parse_sub, parseWx_sub
from crawldata_spider.tools.jsobject import ctx, key
from crawldata_spider.tools import tools, redis_cli


def expansion(lists) -> list:
    res = []
    for i in lists:
        if isinstance(i, list):
            res.extend(expansion(i))
        else:
            res.append(i)
    return res


class Ygp(feapder.AirSpider):
    def start_requests(self):
        total = 200
        page_count = int(total / 20)
        siteCode = '44'
        # secondType = 'A'
        # ["A", "B", "C", "D", "R", "F", "G"]
        secondTypeList = ["A", "B", "C", "D", "R", "F", "G"]
        for second in secondTypeList:
            for i in range(1, page_count):
                json_data = {
                    'type': 'trading-type',
                    'publishStartTime': '',
                    'publishEndTime': '',
                    'siteCode': siteCode,
                    'secondType': second,
                    'projectType': '',
                    'thirdType': '',
                    'dateType': '',
                    'total': 0,
                    #
                    'pageNo': i,
                    'pageSize': 20,
                    'openConvert': False,
                }
                time.sleep(0.5)
                yield feapder.Request("https://ygp.gdzwfw.gov.cn/ggzy-portal/search/v1/items", json=json_data,
                                      method="POST", download_midware=self.download_midware, request_sync=True,
                                      callback=self.parse, pageNo=i,
                                      pageSize=20, secondType=second,
                                      siteCode=siteCode)

    def download_midware(self, request):
        """
        :param request:
        :return:
        """
        random_s = random.sample(string.ascii_letters + string.digits, 16)
        Nonce = ''.join(random_s)
        Timestamp = str(int(time.time() * 1000))
        # 没请求参数的话 一般不加这个东西 （基本就是请求参数） 这个生成签名需要
        t = "dateType=&openConvert=false&pageNo=%s&pageSize=%s&projectType=&publishEndTime=&publishStartTime=&secondType=%s&siteCode=%s&thirdType=&total=0&type=trading-type" % (
            request.pageNo, request.pageSize, request.secondType, request.siteCode)
        Signature = ctx.call('Ig', Nonce + key + t + Timestamp)
        # cookies = {
        #     '_horizon_uid': '6476aa19-0e7b-46a6-bb77-b3648128981c',
        #     '_horizon_sid': '525c2334-2363-4eaf-beb4-255e399ff54b',
        # }
        cookies = {
            '_horizon_uid': 'ac35adbe-438b-424e-b85e-b80416fbabe0',
            '_horizon_sid': 'ee47c33b-a168-44c5-9a16-70ebf5d1bfba',
        }
        request.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://ygp.gdzwfw.gov.cn',
            'Referer': 'https://ygp.gdzwfw.gov.cn/ggzy-portal/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'X-Dgi-Req-App': 'ggzy-portal',
            'X-Dgi-Req-Nonce': Nonce,
            'X-Dgi-Req-Signature': Signature,
            'X-Dgi-Req-Timestamp': Timestamp,
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        # request.cookies = cookies
        # pro = tools.get_proxy()
        # request.proxies = pro
        return request

    def parse(self, request, response):
        res = json.loads(response.text)
        if res.get('data'):
            res = res.get('data')
        for i in res.get("pageData"):
            noticeSecondType = i.get("noticeSecondType")
            projectCode = i.get("projectCode")
            tradingProcess = i.get("tradingProcess")
            siteCode = i.get("siteCode")
            data = {
                'tradingType': noticeSecondType,
                'projectCode': projectCode,
                'tradingProcess': tradingProcess,
                'siteCode': siteCode,
            }
            t = "projectCode=%s&siteCode=%s&tradingProcess=%s&tradingType=%s" % (
                projectCode, siteCode, tradingProcess, noticeSecondType)

            cnd = {}
            noticeSecondTypeDesc = i.get("noticeSecondTypeDesc", "")
            if noticeSecondTypeDesc in ("工程建设", "土地矿业", "国有产权", "政府采购", "排污权", "林权交易"):
                if noticeSecondTypeDesc == "林权交易":
                    noticeSecondTypeDesc = "林权"
                if noticeSecondTypeDesc == "土地矿业":
                    if i.get("projectTypeName") == "土地使用权交易":
                        noticeSecondTypeDesc = "土地使用"
                    if i.get("projectTypeName") == "采矿权出让":
                        noticeSecondTypeDesc = "矿业产权"
            else:
                noticeSecondTypeDesc = "其他"
            noticeThirdTypeDesc = i.get("noticeThirdTypeDesc", "")
            if noticeThirdTypeDesc in ("招标公告与资格预审公告", "出让公告", "预披露公告", "资格预审公告", "采购公告", "交易公告", "信息披露"):
                noticeThirdTypeDesc = "招标公告"
            elif noticeThirdTypeDesc in (
                    "中标结果", "成交公示", "中标（成交）结果公告", "中选公告", "结果公告", "成交公告", "中标结果公告", "中标候选人公示", "评标报告"):
                noticeThirdTypeDesc = "中标公告"
            else:
                noticeThirdTypeDesc = "其他公告"

            publishDate = i.get("publishDate", "")
            if not publishDate:
                # 默认时间
                newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:
                newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(publishDate, "%Y%m%d%H%M%S"))
            except Exception as e:
                print("时间格式转化err", e)
            cnd["industry_classification"] = noticeSecondTypeDesc
            cnd["city"] = i.get("siteName")
            cnd["title"] = i.get("noticeTitle")
            cnd["bulletinType"] = noticeThirdTypeDesc
            cnd["publishDate"] = newtime
            if not redis_cli.get_cache("ygp_" + i.get("noticeTitle")):
                # redis_cli.set_cache("stop", 1)
                print("详情抓取------->", cnd)
                yield feapder.Request('https://ygp.gdzwfw.gov.cn/ggzy-portal/center/apis/trading-notice/detail',
                                      params=data, method="GET",
                                      download_midware=self.details_dm, request_sync=True,
                                      callback=self.details_pm, t=t, cnd=cnd)

    def details_dm(self, request):
        # request.cookies = {
        #     '_horizon_uid': 'ac35adbe-438b-424e-b85e-b80416fbabe0',
        #     '_horizon_sid': 'a7a555cb-6c3c-492c-b392-e373598df94a',
        # }
        cookies = {
            '_horizon_uid': 'ac35adbe-438b-424e-b85e-b80416fbabe0',
            '_horizon_sid': 'ee47c33b-a168-44c5-9a16-70ebf5d1bfba',
        }
        random_s = random.sample(string.ascii_letters + string.digits, 16)
        Nonce = ''.join(random_s)
        Timestamp = str(int(time.time() * 1000))
        t = request.t
        Signature = ctx.call('Ig', Nonce + key + t + Timestamp)
        request.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://ygp.gdzwfw.gov.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'X-Dgi-Req-App': 'ggzy-portal',
            'X-Dgi-Req-Nonce': Nonce,
            'X-Dgi-Req-Signature': Signature,
            'X-Dgi-Req-Timestamp': Timestamp,
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        pro = tools.get_proxy()
        request.proxies = pro
        # request.cookies = cookies
        return request

    def details_pm(self, request, response):
        res = json.loads(response.text)
        if res.get('data'):
            res = res.get('data')
        if isinstance(res, list):
            # 嵌套列表展开
            res = expansion(res)
            for i in res:
                Content = ""
                if request.cnd.get("industry_classification") in ("工程建设", "政府采购", "排污权"):
                    if i.get("noticeContent", ""):
                        Content = i.get("noticeContent", "")
                    if i.get("publicityContent", ""):
                        Content = i.get("publicityContent", "")
                elif request.cnd.get("industry_classification") in ("土地使用", "矿业产权", "国有产权"):
                    Content = i.get("announcementConnect", "")
                amount = re.search("招标部分估价.*?元", Content)
                contact_content = re.search("<b>招标人与招标代理</b>.*?<b>", Content)
                contact_content = contact_content[0] if contact_content else ""
                contact_person = re.search("经办人.*?<", contact_content)
                contact_information1 = re.search("办公电话.*?<", contact_content)
                contact_information2 = re.search("手机号码.*?<", contact_content)
                contact_information = ""
                if amount:
                    amount = amount[0].split("：")[-1].replace(" ", "")
                if contact_person:
                    contact_person = contact_person[0].split("：")[-1].replace("<", "").replace(" ", "")
                if contact_information1:
                    contact_information1 = contact_information1[0].split("：")[-1].replace("<", "").replace(" ", "")
                    contact_information = contact_information1
                if contact_information2:
                    contact_information2 = contact_information2[0].split("：")[-1].replace("<", "").replace(" ", "")
                    contact_information = contact_information2
                if contact_information1 and contact_information2:
                    contact_information = contact_information1 + " / " + contact_information2
                Content = tools.filterHtmlTag(Content)
                abstract = tools.text_abstract(Content)

                data = {}
                data.setdefault("bulletin_type", request.cnd.get("bulletinType", "其他公告"))
                data.setdefault("city", request.cnd.get("city", ""))
                data.setdefault("title", i.get("noticeName") if i.get("noticeName") else request.cnd.get("title", ""))
                data.setdefault("industry_classification", request.cnd.get("industry_classification", "其他"))
                data.setdefault("release_time", request.cnd.get("publishDate", ""))
                data.setdefault("bidopening_time", i.get("bidDocReferEndTime", ""))
                data.setdefault("announcement_content", Content if Content else "")
                data.setdefault("attachment", ",".join([i.get("url") for i in i.get("noticeFileBOList")]) if i.get(
                    "noticeFileBOList") and len(i.get("noticeFileBOList")) < 5 else "")
                data.setdefault("amount", amount if amount else "")
                data.setdefault("contact_person", contact_person if contact_content else "")
                data.setdefault("contact_information", contact_information if contact_information else "")
                data.setdefault("link", i.get("url") if i.get("url") else "")
                data.setdefault("abstract", abstract if abstract else "")
                data.setdefault("enterprise", i.get("winBidderName") if i.get("winBidderName", "") else "")
                data.setdefault("bid_amount", i.get("bidAmount") if i.get("bidAmount", "") else "")
                data.setdefault("tender_name", i.get("tenderAgencyName") if i.get("tenderAgencyName", "") else "")
                data.setdefault("created_at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                insert_ignore = False
                sql = "insert%s into `{table}` {keys} values {values}" % (
                    " ignore" if insert_ignore else ""
                )
                keys = ["`{}`".format(key) for key in data.keys()]
                keys = list2str(keys).replace("'", "")
                values = [format_sql_value(value) for value in data.values()]
                values = list2str(values)
                sql = sql.format(table="bidding", keys=keys, values=values).replace("None", "")
                print(sql)
                _, id = MysqlDb().add(sql)
                if id:
                    print(id)
                    push(data, id)
                    print("开始微信订阅------------------->")
                    for sub in parseWx_sub():
                        print("微信id----------->", sub)
                        if data.get("bulletin_type") == sub[1]:
                            if data.get("city") in sub[2]:
                                for i in sub[3].split(","):
                                    match = re.search("%s.*?" % i, Content)
                                    print("match--------->", match)
                                    if match:
                                        send_messages(to=sub[0], sub_type=sub[1], title=data.get("title"), keywords=i,
                                                      city=data.get("city"),
                                                      sql_id=id, message_type="wx")
                    print("开始个人中心订阅------------------->")
                    for sub in parse_sub():
                        print("用户id----------->", sub)
                        if data.get("bulletin_type") == sub[1]:
                            if data.get("city") in sub[2]:
                                for i in sub[3].split(","):
                                    match = re.search("%s.*?" % i, Content)
                                    print("match--------->", match)
                                    if match:
                                        send_messages(sub[0], sub_type=sub[1], title=data.get("title"), keywords=i,
                                                      city=data.get("city"),
                                                      sql_id=id)
                    redis_cli.set_cache("ygp_" + data.get("title"), 1, ex=60 * 60 * 24 * 7)




if __name__ == "__main__":
    Ygp(thread_count=1).start()
