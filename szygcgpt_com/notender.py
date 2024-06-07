import datetime
import os
import re
import sys
import time

import json
import feapder
from feapder import Item

import tools

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from crawldata_spider.tools.zinc import push
from crawldata_spider.tools.db import MysqlDb
from crawldata_spider.tools.tools import list2str, format_sql_value, parse_sub, parseWx_sub
from crawldata_spider.tools.jsobject import ctx, key
from crawldata_spider.tools import tools, redis_cli
from crawldata_spider.tools.message import send_messages


class YGCG_NoTender(feapder.AirSpider):
    def start_requests(self):
        url = "https://www.szygcgpt.com/app/home/pageGGList.do"
        for lx in range(1, 9):  # 类型 1-8
            for page in range(1, 2):
                data = {
                    # 页数
                    "page": page,
                    # 页大小
                    "rows": 100,
                    "xmLeiXing": "",
                    # 招标0 非招标1
                    "caiGouType": 0,
                    # 类型 1-8
                    "ggLeiXing": lx,
                    "isShiShuGuoQi": "",
                    "isZhanLueYingJiWuZi": "",
                    "keyWords": ""
                }
                data = json.dumps(data, separators=(',', ':'))

                yield feapder.Request(url, data=data, method="POST", lx=lx, request_sync=True)

    def download_midware(self, request):
        request.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.szygcgpt.com",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }

        pro = tools.get_proxy()
        request.proxies = pro
        return request

    def parse(self, request, response):

        lx = request.lx
        """
        采购公告：招标公告
        定标结果公示 :中标公告
        """
        zhaobiao_lx = ["采购公告", "变更公告", "候选人公示", "定标结果公示", "结果公示", "单一来源/邀请公示", "工程变更公示", "合同续期公示"]
        res = json.loads(response.text)
        if res.get("data", None):
            res = res.get("data")
            if res.get("list", None):
                for data in res.get("list"):
                    if data:
                        info = {}
                        # if zhaobiao_lx[lx - 1] == "采购公告":
                        #     info["bulletin_type"] = "招标公告"
                        # elif zhaobiao_lx[lx - 1] == "定标结果公示":
                        #     info["bulletin_type"] = "中标公告"
                        # else:
                        #     info["bulletin_type"] = "其他公告"
                        info["bulletin_type"] = "其他公告"
                        info["city"] = "深圳市"
                        info["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        info["title"] = data["ggName"]
                        ggGuid = data["ggGuid"]
                        bdGuid = data["bdGuid"]
                        ggLeiXing = data["ggLeiXing"]
                        dataSource = data["dataSource"]
                        info[
                            "link"] = f"https://www.szygcgpt.com/ygcg/detailTop?com=Purchase&ggGuid={ggGuid}&bdGuid={bdGuid}&ggLeiXing={ggLeiXing}&dataSource={dataSource}&type=purchase"
                        _t = int(time.time())
                        link = f"https://www.szygcgpt.com/app/etl/detail?_t={_t}&ggGuid={ggGuid}&bdGuid={bdGuid}&ggLeiXing={ggLeiXing}"
                        timeStamp = data["last_update_time"]
                        timeArray = time.localtime(int(timeStamp) / 1000)
                        info["release_time"] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                        if data["xmLeiXing"] == 1:
                            info["industry_classification"] = "工程建设"
                        else:
                            info["industry_classification"] = "其他"
                        if not redis_cli.get_cache("ygcg_" + info["title"]):
                            yield feapder.Request(link, callback=self.parse_details,
                                                  meta=info, download_midware=self.download_midware, request_sync=True)

    def parse_details(self, request, response):
        info = request.meta
        res = json.loads(response.text)
        if res.get("data", None):
            res = res.get("data")
            try:
                contact_person = res["gc"]["lianXiRenName"]
            except:
                contact_person = ""
            try:
                contact_information = res["gc"]["lianXiRenPhone"]
            except:
                contact_information = ""

            try:
                tender_name = res["gc"]["zbrName"]
            except:
                tender_name = ""

            try:
                bidopening_time = res["bd"]["kbTime"]
                timeArray = time.localtime(int(bidopening_time) / 1000)
                bidopening_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            except:
                bidopening_time = ""

            try:
                amount = res["bd"]["bdHeTongGuJia"]
            except:
                amount = ""

            # zbFanWei
            try:
                zbFanWei = res["bd"]["zbFanWei"]
            except:
                zbFanWei = ""

            # ziZhiYaoQiu

            try:
                ziZhiYaoQiu = res["bd"]["ziZhiYaoQiu"]
            except:
                ziZhiYaoQiu = ""

            # ggDetail -> pingBiaoJieGuoVoList
            try:
                winbid = res["ggDetail"]["pingBiaoJieGuoVoList"]
                for win in winbid:
                    if win.get("zhongBiaoJia", ""):
                        winName = win.get("tbrName", "")
                        bidamont = win.get("zhongBiaoJia", "")
            except:
                winName = ""
                bidamont = ""
            # ggDetail -> fileList
            # https://www.szygcgpt.com/
            try:
                files = res["ggDetail"]["fileList"]
                attachment = ",".join(["https://www.szygcgpt.com/"+file.get("fileUrl") for file in files])
            except:
                attachment = ""

            Content = zbFanWei + ziZhiYaoQiu
            info["amount"] = amount
            info["contact_person"] = contact_person
            info["contact_information"] = contact_information
            info["bidopening_time"] = bidopening_time
            info["tender_name"] = tender_name
            abstract = tools.text_abstract(Content)
            info["announcement_content"] = Content
            info["abstract"] = abstract
            info["enterprise"] = winName
            info["bid_amount"] = bidamont
            info["attachment"] = attachment
            data = info
            print(info)
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
                            match = re.search("%s.*?" % sub[3], Content)
                            print("match--------->", match)
                            if match:
                                send_messages(to=sub[0], sub_type=sub[1], title=data.get("title"), keywords=sub[3],
                                              city=data.get("city"),
                                              sql_id=id, message_type="wx")
                print("开始个人中心订阅------------------->")
                for sub in parse_sub():
                    print("用户id----------->", sub[0])
                    if data.get("bulletin_type") == sub[1]:
                        if data.get("city") in sub[2]:
                            match = re.search("%s.*?" % sub[3], Content)
                            print("match--------->", match)
                            if match:
                                send_messages(sub[0], sub_type=sub[1], title=data.get("title"), keywords=sub[3],
                                              city=data.get("city"),
                                              sql_id=id)
                redis_cli.set_cache("ygcg_" + data.get("title"), 1, ex=60 * 60 * 24 * 3)
        else:
            print("no data res----->", res)
            time.sleep(1)


if __name__ == "__main__":
    YGCG_NoTender(thread_count=1).start()
