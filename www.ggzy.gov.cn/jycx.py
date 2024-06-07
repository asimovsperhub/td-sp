import datetime
import feapder
from feapder import Item
from lxml import etree


class AirSpiderJycx(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):
        url = "http://www.ggzy.gov.cn/information/credit/creditList.jsp"
        for i in range(1,3):
            if i==1:
                cs="违法违规"
            else:
                cs="奖励信息"
            for page in range(1,2):
                data = {
                    "SHOWTYPE": str(i),
                    "PAGENUMBER": str(page),
                    "findtxt": ""
                }
                yield feapder.Request(url, data=data, method="POST", cs=cs)


    def download_midware(self, request):
        '''
                          下载中间件
                            :return:
                   '''
        request.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://deal.ggzy.gov.cn",
            "Referer": "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
}

        return request

    def parse(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        html = response.text
        res = etree.HTML(html)
        trs = res.xpath('//ul[@class="ullist"]/li')
        for tr in trs:
            info = {}
            info["block"] = "交易诚信"
            info["collet_area"] = request.cs
            info["collet_area2"] =""
            info["plate"] = "政策资讯"
            info["pulic_type"] = "最新资讯"
            info["province"] =""
            info["city"] = ""
            info["field"] =""
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info["title"] = tr.xpath('./a/@title')[0]
            info[ "file_link"] =tr.xpath('./a/@href')[0]
            info["public_time"] = tr.xpath('./span/text()')[0]
            yield feapder.Request(info[ "file_link"], callback=self.down_file1,
                                  meta=info)
            break

    def down_file1(self, request, response):
        '''
                   解析公告
                    :return:
           '''
        info = request.meta
        html = response.text
        res = etree.HTML(html)

        trs = res.xpath('//div[@class="creditDetail"]//text()')
        info["public_text"] = "".join(trs).replace('分享到微信 ','').replace('用微信“扫一扫”，点击右上角分享按钮，即可将网页分享给您的微信好友或朋友圈','')
        info["html"] = html
        contact = " "
        contact_number = " "
        money = " "
        info["contact"] = contact
        info["contact_number"] = contact_number
        info["money"] = money
        item = Item()
        item.table_name = "ggzy"  # 表名
        item.block = info["block"]
        item.collet_area = info["collet_area"]
        item.collet_area2 = info["collet_area2"]
        item.plate = info["plate"]
        item.pulic_type = info["pulic_type"]
        item.city = info["city"]
        item.field = info["field"]
        item.create_time = info["create_time"]
        item.title = info["title"]
        item.file_link = info["file_link"]
        item.public_time = info["public_time"]
        item.province = info["province"]
        item.public_text = info["public_text"]
        item.html = info["html"]
        item.contact = info["contact"]
        item.contact_number = info["contact_number"]
        item.money = info["money"]

        yield item



if __name__ == "__main__":
    AirSpiderJycx(thread_count=1).start()
