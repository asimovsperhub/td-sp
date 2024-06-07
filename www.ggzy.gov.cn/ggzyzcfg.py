import datetime
import feapder
from feapder import Item
from lxml import etree


class AirSpiderZcfg(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):
        url_list= ["http://www.ggzy.gov.cn/information/info/zcwj00/policyList.shtml","http://www.ggzy.gov.cn/information/info/zcjd/policyList.shtml"]
        for url in url_list:
            if url=="http://www.ggzy.gov.cn/information/info/zcwj00/policyList.shtml":
                for page in range(1,4):
                    if page==1:
                        url="http://www.ggzy.gov.cn/information/info/zcwj00/policyList.shtml"
                    else:
                        url=f"http://www.ggzy.gov.cn/information/info/zcwj00/policyList_{page}.shtml"

                    yield feapder.Request(url, verify=False, method="GET",cs="政策法规文件",lx="法律法规")

            else:
                for page in range(1,3):
                    if page==1:
                        url="http://www.ggzy.gov.cn/information/info/zcjd/policyList.shtml"
                    else:
                        url=f"http://www.ggzy.gov.cn/information/info/zcjd/policyList_{page}.shtml"
                    yield feapder.Request(url, verify=False, method="GET",cs="政策法规解读",lx="政策解读")





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
        trs = res.xpath('//ul[@id="contextId"]/li')
        for tr in trs:
            info = {}
            info["pulic_type"] =request.lx
            info["province"] =""
            info["city"] = ""
            info["field"] =""
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info["title"] = tr.xpath('./a/text()')[0]
            info[ "file_link"] =tr.xpath('./a/@href')[0]
            info["public_time"] = tr.xpath('./span/text()')[0]
            yield feapder.Request(info[ "file_link"], callback=self.down_file1,
                                  meta=info)


    def down_file1(self, request, response):
        '''
                   解析公告
                    :return:
           '''
        info = request.meta
        html = response.text
        res = etree.HTML(html)

        trs = res.xpath('//div[@class="ultimately"]//text()')
        info["public_text"] = "".join(trs).replace('分享到微信 ','').replace('用微信“扫一扫”，点击右上角分享按钮，即可将网页分享给您的微信好友或朋友圈','')
        # info["html"] = html
        item = Item()
        item.table_name = "consultation"  # 表名
        item.type = info["pulic_type"]
        item.created_at = info["create_time"]
        item.title = info["title"]
        item.url = info["file_link"]
        item.publish = info["public_time"].replace("\r","").replace("\n","") if info["public_time"] else ""
        item.content = info["public_text"]
        # print(item)

        yield item



if __name__ == "__main__":
    AirSpiderZcfg(thread_count=1).start()
