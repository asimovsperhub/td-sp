import datetime
import time
import re
import feapder
from feapder import Item
from lxml import etree

now = time.time()
timeArray = time.localtime(now)
nowtime = time.strftime("%Y-%m-%d", timeArray).replace("-", ":")
import tools


class AirSpiderCggg(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''

    def start_requests(self):

        for lx in range(1, 13):
            url = "http://search.ccgp.gov.cn/bxsearch"
            pages = int(92600/20)
            for page in range(1, pages):
                params = {
                    "searchtype": "1",
                    "page_index": str(page),
                    "bidSort": "0",
                    "buyerName": "",
                    "projectId": "",
                    "pinMu": "0",
                    "bidType": "1",
                    "dbselect": "bidx",
                    "kw": "",
                    "start_time": "2022:03:05",
                    "end_time": "2023:03:05",
                    "timeType": "0",
                    "displayZone": "",
                    "zoneId": "",
                    "pppStatus": "0",
                    "agentName": ""
                }

                yield feapder.Request(url, params=params, verify=False, method="GET", lx=lx, count=1)

    def download_midware(self, request):
        '''
                          下载中间件
                            :return:
                   '''
        request.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "$Cookie": "HMF_CI=c073a0a042ff7ecb18b1b632111d56074aedbbb2a8b74eb73c58fefef1dbe861352a61a7662855ff2a70ddb1c6e4935e4fbc26287a635b0968424728d9e64de63e; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1677002480,1677002600; HMY_JC=f4c29e36f7345cb0b7633bf06d247238504ffb80a93547445c885a65d96155670b,; HBB_HC=5d434950322ef2b233bd2430de59a9f4b72351343bd805646512902d9f811c6d0d48527ab9edb88617c2bc0b24e3ffbbc7; JSESSIONID=6nR1Le_X1dsJ3A9v1CDJwAKTV4UAJcEH2vF_4MiveGR0X5nQJRCZ\\u00211144578798; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1677003190",
            "Pragma": "no-cache",
            "Referer": "http://search.ccgp.gov.cn/znzxsearch?searchtype=1&page_index=2&searchchannel=1&kw=&start_time=&end_time=&timeType=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        # request.proxies = {"http": "http://127.0.0.1:10809",
        #      "https": "http://127.0.0.1:10809"}

        return request

    def parse(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        lx = request.lx
        count = request.count
        zx_list = ["公开招标", "询价公告", "竞争性谈判", "单一来源", "资格预审", "邀请公告", "中标公告", "更正公告", "其他公告", "竞争性磋商", "成交公告", "终止公告"]
        html = response.text
        try:
            page = int(re.findall("size: (.*?),", html)[0])
        except:
            page = 1
        html = etree.HTML(html)
        trs = html.xpath('//ul[@class="vT-srch-result-list-bid"]/li')
        for tr in trs:
            info = {}
            info["block"] = "采购公告"
            info["collet_area"] = zx_list[lx - 1]
            info["collet_area2"] = ""
            info["plate"] = "招标信息"
            if info["collet_area"] == "公开招标":
                info["pulic_type"] = "招标公告"
            elif info["collet_area"] == "询价公告":
                info["pulic_type"] = "意向公开"
            elif info["collet_area"] == "中标公告":
                info["pulic_type"] = "中标公告"
            else:
                info["pulic_type"] = "其他公告"
            info["city"] = ""
            info["field"] = ""
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = tr.xpath('./a/text()')[0].replace(" ", "").replace("\r\n", "")
            info["file_link"] = tr.xpath('./a/@href')[0]
            info["public_time"] = tr.xpath('./span/text()')[0].split("\r")[0]
            try:
                info["province"] = tr.xpath('./span/a/text()')[0]
            except:
                info["province"] = " "

            yield feapder.Request(info["file_link"], callback=self.down_file, meta=info)
        # 翻页
        if count < int(page) + 1:
            count += 1
            url = "http://search.ccgp.gov.cn/bxsearch"
            params = {
                "searchtype": "1",
                "page_index": str(count),
                "bidSort": "0",
                "buyerName": "",
                "projectId": "",
                "pinMu": "0",
                "bidType": "1",
                "dbselect": "bidx",
                "kw": "",
                "start_time": nowtime,
                "end_time": nowtime,
                "timeType": "0",
                "displayZone": "",
                "zoneId": "",
                "pppStatus": "0",
                "agentName": ""
            }
            yield feapder.Request(url, params=params, verify=False, method="GET", lx=lx, count=count)

    def down_file(self, request, response):
        info = request.meta
        html = response.content.decode("utf-8")
        info["html"] = html
        res = etree.HTML(html)
        trs = res.xpath('//div[@class="vF_detail_content"]//text()')
        info["public_text"] = "".join(trs)
        html_text = ""
        if html:
            html_text = tools.filterHtmlTag(html)
        amount = re.search("预算金额.*?元", html_text)
        contact_person = re.search("联系人：.*?[\u4e00-\u9fa5]+", html_text)
        contact_information = re.search("电*话：.*?[0-9a-zA-Z\-]+", html_text)
        if amount:
            amount = amount[0].split("：")[-1]
        if contact_person:
            contact_person = contact_person[0].split("：")[-1]
        if contact_information:
            contact_information = contact_information[0].split("：")[-1]
        # 提交投标文件截止时间
        # <re.Match object; span=(1534, 1550), match='开标时间：2023年03月27日'>
        bidopening_time = re.search("开标时间：.*?\d{4}年\d{1,2}月\d{1,2}日", html_text)
        if bidopening_time:
            bidopening_time = bidopening_time[0].replace("开标时间：", "")
        if not bidopening_time:
            # 开标时间和地点
            bidopening_time = re.search("开标时间和地点.*?\d{4}年\d{1,2}月\d{1,2}日", html_text)
            if bidopening_time:
                bidopening_time = re.search("\d{4}年\d{1,2}月\d{1,2}日", bidopening_time[0])
                bidopening_time = bidopening_time[0] if bidopening_time else None
        item = Item()
        item.table_name = "bidding_information"
        item.bulletin_type = info.get("block", "")
        item.notice_nature = info.get("pulic_type", "")
        item.city = info.get("city", "")
        item.release_time = info.get("public_time", "")
        # item.tender_deadline = i.get("bidClosingTime")
        item.title = info.get("title", "")
        # item.attachment = info.get("file_link", "")
        item.industry_classification = info.get("field", "")
        item.announcement_content = info.get("html", "")
        item.link = info.get("file_link", "")
        item.amount = amount
        item.contact_person = contact_person
        item.contact_information = contact_information
        item.bidopening_time = bidopening_time
        yield item


if __name__ == "__main__":
    AirSpiderCggg(thread_count=1).start()
