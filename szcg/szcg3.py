import datetime
import re

import feapder
from feapder import Item
from lxml import etree

import tools


class AirSpiderDemo(feapder.AirSpider):
    def start_requests(self):
        url = "https://www.szzfcg.cn/portal/topicView.do"
        params = {
            "method": "view",
            "id": "2014"
        }
        for page in range(1, 1511):
            data = {
                "ec_i": "topicChrList_20070702",
                "topicChrList_20070702_crd": "100",
                "topicChrList_20070702_f_a": "",
                "topicChrList_20070702_p": str(page),
                "topicChrList_20070702_s_webName": "",
                "topicChrList_20070702_s_name": "",
                "topicChrList_20070702_s_speciesCategory": "",
                "topicChrList_20070702_s_ldate": "",
                "id": "2014",
                "method": "view",
                "__ec_pages": str(page),
                "topicChrList_20070702_rd": "100",
                "topicChrList_20070702_f_webName": "",
                "topicChrList_20070702_f_name": "",
                "topicChrList_20070702_f_speciesCategory": "",
                "topicChrList_20070702_f_ldate": ""
            }

            yield feapder.Request(url, params=params, data=data, method="POST")

    def download_midware(self, request):
        request.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "$Cookie": "JSESSIONID=EhlKUyayIdLse3-jh38_PON7Y62oCsR5mgubZndPLd9bOnkOWh8U\\u0021-1177488671\\u00212092975900",
            "Origin": "https://www.szzfcg.cn",
            "Pragma": "no-cache",
            "Referer": "https://www.szzfcg.cn/stock/stprFile.do?method=listSy&siteId=1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        pro = tools.get_proxy()
        request.proxies = pro
        return request

    def parse(self, request, response):
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//tbody[@class="tableBody"]/tr')
        for tr in trs:
            info = {}
            info["block"] = "采购结果公示"
            info["plate"] = "招标信息"
            info["pulic_type"] = "中标公告"
            info["city"] = "深圳"
            info["field"] = "其他"
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info["filename"] = ""
            link = tr.xpath(".//a/@href")[0]
            id = re.findall("id=(.*)", link)[0]
            info["file_link"] = f"https://www.szzfcg.cn/portal/documentView.do?method=view&id={id}"
            info["public_time"] = tr.xpath("./td[5]/text()")[0]
            info["title"] = tr.xpath(".//a/text()")[0]
            info["pinmu"] = tr.xpath("./td[4]/text()")[0]
            if info["pinmu"] == '\xa0':
                info["pinmu"] = " "
            info["area"] = tr.xpath("./td[2]/text()")[0]
            info["province"] = "广东"

            yield feapder.Request(info["file_link"], callback=self.down_file,
                                  meta=info)

    def down_file(self, request, response):
        info = request.meta
        html = response.text
        info["html"] = html
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
        yield item


if __name__ == "__main__":
    AirSpiderDemo(thread_count=1).start()
