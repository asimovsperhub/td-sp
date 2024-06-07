import datetime
import time

import json
import feapder
from feapder import Item

import tools


class AirSpiderZhaobiao(feapder.AirSpider):
    def start_requests(self):
        url = "https://www.szygcgpt.com/app/home/pageGGList.do"
        for lx in range(1, 9):  # 类型 1-8
            if lx == 1:
                count_page = 316
            if lx == 2:
                count_page = 71
            if lx == 3:
                count_page = 376
            if lx == 4:
                count_page = 33
            if lx == 5:
                count_page = 412
            if lx == 6:
                count_page = 105
            if lx == 7:
                count_page = 3
            if lx == 8:
                count_page = 8
            for page in range(1, 5):
                data = {
                    "page": page,
                    "rows": 100,
                    "xmLeiXing": "",
                    "caiGouType": 1,
                    "ggLeiXing": lx,
                    "isShiShuGuoQi": "",
                    "isZhanLueYingJiWuZi": "",
                    "keyWords": ""
                }
                data = json.dumps(data, separators=(',', ':'))

                yield feapder.Request(url, data=data, method="POST", lx=lx)

    def download_midware(self, request):
        '''
                          下载中间件
                            :return:
                   '''
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
        '''
                            解析页面
                            :return:
                   '''
        lx = request.lx
        zhaobiao_lx = ["采购公告", "变更公告", "候选人公示", "定标结果公示", "结果公示", "单一来源/邀请公示", "工程变更公示", "合同续期公示"]
        if len(response.text) > 500:
            json_data = json.loads(response.text)["data"]["list"]
            for data in json_data:
                info = {}
                info["block"] = "交易信息"
                info["collet_area"] = "招标"
                info["collet_area2"] = zhaobiao_lx[lx - 1]
                info["plate"] = "招标信息"
                info["pulic_type"] = "招标公告"
                info["city"] = "深圳"
                info["field"] = "其他"
                info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                info["title"] = data["ggName"]
                ggGuid = data["ggGuid"]
                bdGuid = data["bdGuid"]
                ggLeiXing = data["ggLeiXing"]
                dataSource = data["dataSource"]
                info[
                    "file_link"] = f"https://www.szygcgpt.com/ygcg/detailTop?com=Purchase&ggGuid={ggGuid}&bdGuid={bdGuid}&ggLeiXing={ggLeiXing}&dataSource={dataSource}&type=purchase"
                _t = int(time.time())
                link = f"https://www.szygcgpt.com/app/etl/detail?_t={_t}&ggGuid={ggGuid}&bdGuid={bdGuid}&ggLeiXing={ggLeiXing}"
                timeStamp = data["last_update_time"]
                timeArray = time.localtime(int(timeStamp) / 1000)
                info["public_time"] = time.strftime("%Y-%m-%d", timeArray)

                yield feapder.Request(link, callback=self.down_file1,
                                      meta=info)

    def down_file1(self, request, response):
        '''
                   解析公告
                    :return:
           '''
        info = request.meta
        html = response.text
        # info["html"]=html
        info["public_text"] = html

        try:
            contact = json.loads(html)["data"]["gc"]["lianXiRenName"]
        except:
            contact = " "
        try:
            contact_number = json.loads(html)["data"]["gc"]["lianXiRenPhone"]
            kbTime = json.loads(html)["data"]["bd"]["kbTime"]
        except:
            contact_number = " "
        try:
            kbTim = json.loads(html)["data"]["bd"]["kbTime"]
            timeArray = time.localtime(int(kbTim) / 1000)
            kbTime = time.strftime("%Y-%m-%d", timeArray)
        except:
            kbTime = " "
        try:
            money = json.loads(html)["data"]["bd"]["bdHeTongGuJia"]
        except:
            money = " "
        info["province"] = "广东"
        item = Item()
        item.table_name = "bidding_information"
        item.bulletin_type = info.get("block", "")
        item.notice_nature = info.get("pulic_type", "")
        item.city = info.get("city", "")
        item.release_time = info.get("public_time", "")
        # item.tender_deadline = i.get("bidClosingTime")
        item.title = info.get("title", "")
        item.attachment = info.get("file_link", "")
        item.industry_classification = info.get("field", "")
        item.announcement_content = info.get("html", "")
        item.link = info.get("file_link", "")
        item.amount = money
        item.contact_person = contact
        item.contact_information = contact_number
        item.bidopening_time = kbTime
        print(item)


if __name__ == "__main__":
    AirSpiderZhaobiao(thread_count=1).start()
