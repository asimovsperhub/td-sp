import datetime
import re

import feapder
from feapder import Item
from lxml import etree
import tools

"""
意向公告
"""


class AirSpiderYxgg(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''

    def start_requests(self):
        url_list = ["http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001001/list.html",
                    "http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001002/purchase_intention.html"]
        for url in url_list:
            # 2022 之前
            if url == "http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001001/list.html":
                for page in range(1, 13):
                    if page == 1:
                        url = "http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001001/list.html"
                    else:
                        url = f"http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001001/{page}.html"
                    yield feapder.Request(url, callback=self.parse1, verify=False, method="GET")
            # 2022 之后
            else:
                for page in range(1, 1049):
                    url = f"http://zfcg.szggzy.com:8081/gsgg/002001/002001001/002001001002/purchase_intention.html?categoryNum=002001001002&pageIndex={page}"
                    yield feapder.Request(url, callback=self.parse2, verify=False, method="GET")
                    break

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
            "Pragma": "no-cache",
            "Referer": "http://zfcg.szggzy.com:8081/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
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

    def parse1(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        html = response.text
        html = etree.HTML(html)
        # /html/body/div/div[3]/div[2]/div[2]/div
        trs = html.xpath('//div[@class="bid-info"]//li')
        for tr in trs:
            info = {}
            info["block"] = "公示公告"
            info["collet_area"] = "采购意向公开"
            info["plate"] = "招标信息"
            info["pulic_type"] = "意向公开"
            info["city"] = "深圳市"
            info["field"] = "其他"
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = tr.xpath(".//a/@title")[0]
            info["file_link"] = tr.xpath(".//a/@href")[0]
            info["public_time"] = tr.xpath("./span[@class='news-time']/text()")[0].strip()
            info["file"] = " "
            info["money"] = " "
            info["company"] = " "
            yield feapder.Request(info["file_link"], callback=self.down_file1,
                                  meta=info)

    # 采购意向公告
    def parse2(self, request, response):
        '''
                    解析页面
                    :return:
           '''

        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//tbody[@id="list"]//tr')

        for tr in trs:
            info = {}
            info["block"] = "公示公告"
            info["collet_area"] = "采购意向公开"
            info["plate"] = "招标信息"
            info["pulic_type"] = "意向公告"
            info["city"] = "深圳市"
            info["field"] = "其他"
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = tr.xpath("./td[2]/text()")[0]
            info["file_link"] = tr.xpath("./td[7]/a/@href")[0]
            info["public_time"] = tr.xpath("./td[5]/text()")[0].strip()
            info["file"] = " "
            info["money"] = tr.xpath("./td[3]/text()")[0]  # 金额
            info["company"] = tr.xpath("./td[4]/text()")[0]  # 采购单位
            info["purchase"] = tr.xpath("./td[6]/text()")[0]  # 预计采购时间

            yield feapder.Request(info["file_link"], callback=self.down_file2,
                                  meta=info)

    def down_file1(self, request, response):
        '''
                   解析公告
                    :return:
           '''
        info = request.meta
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//tbody//text()')
        text = "".join(trs)
        info["public_text"] = text
        try:
            contact = str(re.findall("联系人(.*)", text)[0]).replace("：", '').replace("，", '')
        except:
            contact = " "
        info["contact"] = contact
        contact_number = " "
        try:
            regular = re.compile(r'\d{3,4}-\d{6,9}|\d{3}-\d{9}')
            contact_number = re.findall(regular, text)[0]
        except:
            number_list = re.findall('(\d+)', text)
            for number in number_list:
                if int(number) > 1000000:
                    contact_number = number
        info["contact_number"] = contact_number
        # 匹配金额
        try:
            number_list = contact_number.split("-")
        except:
            number_list = list(contact_number)

        money = ' '
        try:
            money = re.findall('(\d+\.?\d*)万元', text)[0]
        except:
            year = re.findall('(\d+)年\d+月', text)
            mon = re.findall('\d+年(\d+)月', text) + re.findall('\d+月(\d+)日', text)
            moneys = re.findall(r"\d+\.?\d*", text)
            moneys = list(set(moneys).difference(set(number_list)))
            moneys = list(set(list(set(moneys).difference(set(year)))).difference(mon))
            for money in moneys:
                if float(money) > 10 and int(money[0]) != 0:
                    money = str(float(money))
                    break
        info["money"] = money
        # print(info)

    def down_file2(self, request, response):
        info = request.meta
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//div[@class="contentbox"]//text()')
        info["public_text"] = "\n".join(trs)
        info["contact"] = trs[12]
        info["contact_number"] = trs[14]
        item = Item()
        item.table_name = "bidding_information"
        item.bulletin_type = info.get("pulic_type", "")
        item.notice_nature = info.get("block", "")
        # province
        item.city = info.get("province", "") if info.get("city", "") == "省本级" else info.get("city", "")
        item.release_time = info.get("public_time", "")
        # item.tender_deadline = i.get("bidClosingTime")
        item.title = info.get("title", "")
        # item.attachment = info.get("file_link", "")
        item.industry_classification = "政府采购"
        item.announcement_content = info.get("public_text", "")
        item.link = info.get("file_link", "")
        item.amount = info["money"]
        item.contact_person = info["contact"]
        item.contact_information = info["contact_number"]
        item.bidopening_time = info["purchase"]
        print(item)


if __name__ == "__main__":
    AirSpiderYxgg(thread_count=1).start()
